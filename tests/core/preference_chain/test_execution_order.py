import logging

import pytest

from pyscaf.preference_chain import CircularDependencyError, best_execution_order

logger = logging.getLogger(__name__)


class TestBestExecutionOrder:
    """Test the best_execution_order function directly with the expected input format."""

    def test_simple_linear_execution_order(self):
        """Test simple linear dependency chain using the API format."""
        nodes = [
            {"id": "A", "fullfilled": False, "external": []},
            {"id": "B", "fullfilled": False, "external": ["A"]},
            {"id": "C", "fullfilled": False, "external": ["B"]},
        ]

        result = best_execution_order(nodes)
        expected = ["A", "B", "C"]

        assert result == expected, f"Expected {expected}, got {result}"

    def test_diamond_execution_order(self):
        """Test diamond dependency pattern."""
        nodes = [
            {"id": "A", "fullfilled": False, "external": []},
            {"id": "B", "fullfilled": False, "external": ["A"]},
            {"id": "C", "fullfilled": False, "external": ["A"]},
            {"id": "D", "fullfilled": False, "external": ["B", "C"]},
        ]

        result = best_execution_order(nodes)

        # A should be first, D should be last
        assert result[0] == "A", f"Expected A to be first, got {result}"
        assert result[-1] == "D", f"Expected D to be last, got {result}"

        # Check that dependencies are respected
        a_index = result.index("A")
        b_index = result.index("B")
        c_index = result.index("C")
        d_index = result.index("D")

        assert a_index < b_index and a_index < c_index, "A should come before B and C"
        assert b_index < d_index and c_index < d_index, "B and C should come before D"

    def test_single_dependency_auto_after(self):
        """Test that single dependencies automatically set 'after' preference."""
        nodes = [
            {"id": "root", "fullfilled": False, "external": []},
            {"id": "setup", "fullfilled": False, "external": ["root"]},
            {"id": "build", "fullfilled": False, "external": ["setup"]},
        ]

        result = best_execution_order(nodes)
        expected = ["root", "setup", "build"]

        assert result == expected, f"Expected {expected}, got {result}"

    def test_multiple_external_dependencies(self):
        """Test nodes with multiple external dependencies."""
        nodes = [
            {"id": "A", "fullfilled": False, "external": []},
            {"id": "B", "fullfilled": False, "external": []},
            {"id": "C", "fullfilled": False, "external": ["A", "B"]},
        ]

        result = best_execution_order(nodes)

        # A and B should come before C
        a_index = result.index("A")
        b_index = result.index("B")
        c_index = result.index("C")

        assert a_index < c_index, "A should come before C"
        assert b_index < c_index, "B should come before C"
        assert result[-1] == "C", "C should be last"

    def test_circular_dependency_detection(self):
        """Test that circular dependencies are detected."""
        nodes = [
            {"id": "A", "fullfilled": False, "external": ["B"]},
            {"id": "B", "fullfilled": False, "external": ["C"]},
            {"id": "C", "fullfilled": False, "external": ["A"]},
        ]

        with pytest.raises(CircularDependencyError):
            best_execution_order(nodes)

    def test_complex_real_world_scenario(self):
        """Test a complex scenario resembling real CI/CD pipeline dependencies."""
        nodes = [
            {"id": "checkout", "fullfilled": False, "external": []},
            {"id": "install-deps", "fullfilled": False, "external": ["checkout"]},
            {"id": "lint", "fullfilled": False, "external": ["install-deps"]},
            {"id": "test", "fullfilled": False, "external": ["install-deps"]},
            {"id": "build", "fullfilled": False, "external": ["lint", "test"]},
            {"id": "docker-build", "fullfilled": False, "external": ["build"]},
            {"id": "deploy-staging", "fullfilled": False, "external": ["docker-build"]},
            {"id": "e2e-tests", "fullfilled": False, "external": ["deploy-staging"]},
            {"id": "deploy-prod", "fullfilled": False, "external": ["e2e-tests"]},
        ]

        result = best_execution_order(nodes)

        # Verify key ordering constraints
        checkout_index = result.index("checkout")
        install_deps_index = result.index("install-deps")
        lint_index = result.index("lint")
        test_index = result.index("test")
        build_index = result.index("build")
        docker_build_index = result.index("docker-build")
        deploy_staging_index = result.index("deploy-staging")
        e2e_tests_index = result.index("e2e-tests")
        deploy_prod_index = result.index("deploy-prod")

        # Basic dependency chain
        assert checkout_index < install_deps_index, (
            "checkout should come before install-deps"
        )
        assert install_deps_index < lint_index, "install-deps should come before lint"
        assert install_deps_index < test_index, "install-deps should come before test"
        assert lint_index < build_index and test_index < build_index, (
            "lint and test should come before build"
        )
        assert build_index < docker_build_index, "build should come before docker-build"
        assert docker_build_index < deploy_staging_index, (
            "docker-build should come before deploy-staging"
        )
        assert deploy_staging_index < e2e_tests_index, (
            "deploy-staging should come before e2e-tests"
        )
        assert e2e_tests_index < deploy_prod_index, (
            "e2e-tests should come before deploy-prod"
        )

    def test_empty_input(self):
        """Test with empty input."""
        nodes = []
        result = best_execution_order(nodes)
        assert result == [], "Empty input should return empty result"

    def test_single_node(self):
        """Test with a single node."""
        nodes = [{"id": "single", "fullfilled": False, "external": []}]
        result = best_execution_order(nodes)
        assert result == ["single"], f"Expected ['single'], got {result}"


if __name__ == "__main__":
    # Configure logging for debug mode
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(levelname)s %(name)s::%(funcName)s: \n    %(message)s",
    )

    # Run a simple test
    nodes = [
        {"id": "A", "fullfilled": False, "external": []},
        {"id": "B", "fullfilled": False, "external": ["A"]},
        {"id": "C", "fullfilled": False, "external": ["B"]},
    ]

    result = best_execution_order(nodes)
    print(f"Best execution order: {result}")
