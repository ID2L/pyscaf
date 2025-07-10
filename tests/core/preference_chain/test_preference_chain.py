import logging
import os
from typing import List

import pytest
import yaml

from pyscaf.preference_chain import CircularDependencyError
from pyscaf.preference_chain.chain import (
    build_chains,
    compute_all_resolution_pathes,
    compute_path_score,
    extend_nodes,
)
from pyscaf.preference_chain.dependency_loader import load_and_complete_dependencies

logger = logging.getLogger(__name__)


class PreferenceChainTestHelper:
    """Helper class to test preference chain resolution from YAML files."""

    def __init__(self, test_data_dir: str):
        self.test_data_dir = test_data_dir

    def resolve_dependencies_from_yaml(self, yaml_filename: str) -> List[str]:
        """
        Load dependencies from a YAML file and compute the best execution order.

        Args:
            yaml_filename: Name of the YAML file in the test data directory

        Returns:
            List of node IDs in optimal execution order

        Raises:
            CircularDependencyError: If no valid resolution path can be found
        """
        yaml_path = os.path.join(self.test_data_dir, yaml_filename)

        # Load and complete dependencies from YAML
        dependencies = load_and_complete_dependencies(yaml_path)
        logger.debug(f"Loaded {len(dependencies)} dependencies from {yaml_filename}")

        # Use the preference chain logic
        extended_dependencies = extend_nodes(dependencies)
        clusters = build_chains(extended_dependencies)

        logger.debug(f"Built {len(clusters)} chains")

        # Compute all possible resolution paths
        all_resolution_paths = list(compute_all_resolution_pathes(clusters))

        if not all_resolution_paths:
            # No valid resolution path found
            node_ids = [dep.id for dep in dependencies]
            error_msg = (
                f"No valid resolution path found for nodes: {node_ids}. "
                "This indicates circular dependencies or unsatisfiable constraints."
            )
            logger.error(error_msg)
            raise CircularDependencyError(error_msg)

        logger.debug(f"Found {len(all_resolution_paths)} resolution paths")

        # Sort paths by score (best score first)
        all_resolution_paths.sort(key=lambda path: -compute_path_score(list(path)))

        # Extract the final execution order from the best path
        best_path = all_resolution_paths[0]
        final_order = [node_id for chain in best_path for node_id in chain.ids]

        logger.debug(f"Best execution order: {final_order}")

        return final_order

    def create_yaml_file(self, filename: str, dependencies: List[dict]):
        """Create a YAML file with the given dependencies."""
        yaml_path = os.path.join(self.test_data_dir, filename)
        with open(yaml_path, "w") as f:
            yaml.dump(dependencies, f, default_flow_style=False)


@pytest.fixture
def test_helper():
    """Fixture to provide a test helper with a temporary test data directory."""
    test_data_dir = os.path.join(os.path.dirname(__file__), "test_data")
    os.makedirs(test_data_dir, exist_ok=True)
    return PreferenceChainTestHelper(test_data_dir)


class TestPreferenceChainIntegration:
    """Integration tests for the preference chain resolution mechanism."""

    def test_simple_linear_chain(self, test_helper):
        """Test a simple linear dependency chain: A -> B -> C."""
        dependencies = [
            {"id": "A"},
            {"id": "B", "depends": ["A"]},
            {"id": "C", "depends": ["B"]},
        ]

        test_helper.create_yaml_file("simple_linear.yaml", dependencies)
        result = test_helper.resolve_dependencies_from_yaml("simple_linear.yaml")

        # A should come first, then B, then C
        expected_order = ["A", "B", "C"]
        assert result == expected_order, f"Expected {expected_order}, got {result}"

    def test_diamond_dependency(self, test_helper):
        """Test diamond dependency pattern: A -> B,C -> D."""
        dependencies = [
            {"id": "A"},
            {"id": "B", "depends": ["A"]},
            {"id": "C", "depends": ["A"]},
            {"id": "D", "depends": ["B", "C"]},
        ]

        test_helper.create_yaml_file("diamond.yaml", dependencies)
        result = test_helper.resolve_dependencies_from_yaml("diamond.yaml")

        # A should be first, D should be last, B and C can be in any order in between
        assert result[0] == "A", f"Expected A to be first, got {result}"
        assert result[-1] == "D", f"Expected D to be last, got {result}"
        assert "B" in result and "C" in result, (
            f"Both B and C should be present in {result}"
        )

        # B and C should come after A and before D
        a_index = result.index("A")
        b_index = result.index("B")
        c_index = result.index("C")
        d_index = result.index("D")

        assert a_index < b_index and a_index < c_index, "A should come before B and C"
        assert b_index < d_index and c_index < d_index, "B and C should come before D"

    def test_preference_with_after(self, test_helper):
        """Test preference using 'after' property."""
        dependencies = [
            {"id": "root"},
            {"id": "test", "depends": ["root"]},
            {"id": "coverage", "depends": ["test", "reporting"], "after": "test"},
            {"id": "reporting", "depends": ["root"]},
        ]

        test_helper.create_yaml_file("preference_after.yaml", dependencies)
        result = test_helper.resolve_dependencies_from_yaml("preference_after.yaml")

        # root should be first
        assert result[0] == "root", f"Expected root to be first, got {result}"

        # test should come before coverage (due to 'after' preference)
        test_index = result.index("test")
        coverage_index = result.index("coverage")
        assert test_index < coverage_index, (
            f"test should come before coverage in {result}"
        )

        # reporting should come before coverage (dependency)
        reporting_index = result.index("reporting")
        assert reporting_index < coverage_index, (
            f"reporting should come before coverage in {result}"
        )

    def test_complex_scenario(self, test_helper):
        """Test a more complex scenario similar to the original dependencies.yaml."""
        dependencies = [
            {"id": "root"},
            {"id": "versionning", "depends": ["root"]},
            {"id": "github", "depends": ["versionning"]},
            {"id": "github-actions", "depends": ["github"]},
            {"id": "ci-pipeline", "depends": ["github-actions"]},
            {"id": "pytest", "depends": ["ci-pipeline"]},
            {"id": "coverage", "depends": ["pytest"]},
            {"id": "test", "depends": ["root"]},
            {
                "id": "github-action-test",
                "depends": ["test", "github"],
                "after": "test",
            },
        ]

        test_helper.create_yaml_file("complex.yaml", dependencies)
        result = test_helper.resolve_dependencies_from_yaml("complex.yaml")

        # Validate some key ordering constraints
        assert result[0] == "root", f"Expected root to be first, got {result}"

        # Check dependency chains
        versionning_index = result.index("versionning")
        github_index = result.index("github")
        github_actions_index = result.index("github-actions")
        ci_pipeline_index = result.index("ci-pipeline")
        pytest_index = result.index("pytest")
        coverage_index = result.index("coverage")
        test_index = result.index("test")
        github_action_test_index = result.index("github-action-test")

        # Verify dependency chain: versionning -> github -> github-actions -> ci-pipeline -> pytest -> coverage
        assert (
            versionning_index
            < github_index
            < github_actions_index
            < ci_pipeline_index
            < pytest_index
            < coverage_index
        ), f"Dependency chain violated in {result}"

        # Verify that test comes before github-action-test (after preference)
        assert test_index < github_action_test_index, (
            f"test should come before github-action-test in {result}"
        )

        # Verify that github comes before github-action-test (dependency)
        assert github_index < github_action_test_index, (
            f"github should come before github-action-test in {result}"
        )

    def test_invalid_circular_dependency(self, test_helper):
        """Test that circular dependencies are properly detected and raise an error."""
        dependencies = [
            {"id": "A", "depends": ["B"]},
            {"id": "B", "depends": ["C"]},
            {"id": "C", "depends": ["A"]},
        ]

        test_helper.create_yaml_file("circular.yaml", dependencies)

        with pytest.raises(CircularDependencyError):
            test_helper.resolve_dependencies_from_yaml("circular.yaml")

    def test_single_node(self, test_helper):
        """Test a single node with no dependencies."""
        dependencies = [{"id": "standalone"}]

        test_helper.create_yaml_file("single.yaml", dependencies)
        result = test_helper.resolve_dependencies_from_yaml("single.yaml")

        assert result == ["standalone"], f"Expected ['standalone'], got {result}"

    def test_multiple_roots(self, test_helper):
        """Test multiple independent root nodes."""
        dependencies = [
            {"id": "root1"},
            {"id": "root2"},
            {"id": "child1", "depends": ["root1"]},
            {"id": "child2", "depends": ["root2"]},
        ]

        test_helper.create_yaml_file("multiple_roots.yaml", dependencies)
        result = test_helper.resolve_dependencies_from_yaml("multiple_roots.yaml")

        # Both roots should come before their children
        root1_index = result.index("root1")
        root2_index = result.index("root2")
        child1_index = result.index("child1")
        child2_index = result.index("child2")

        assert root1_index < child1_index, (
            f"root1 should come before child1 in {result}"
        )
        assert root2_index < child2_index, (
            f"root2 should come before child2 in {result}"
        )


if __name__ == "__main__":
    # Configure logging for debug mode
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(levelname)s %(name)s::%(funcName)s: \n    %(message)s",
    )

    # Run a simple test
    test_data_dir = os.path.join(os.path.dirname(__file__), "test_data")
    os.makedirs(test_data_dir, exist_ok=True)
    helper = PreferenceChainTestHelper(test_data_dir)

    # Test the simple linear case
    dependencies = [
        {"id": "A"},
        {"id": "B", "depends": ["A"]},
        {"id": "C", "depends": ["B"]},
    ]
    helper.create_yaml_file("example.yaml", dependencies)
    result = helper.resolve_dependencies_from_yaml("example.yaml")
    print(f"Resolution order: {result}")
