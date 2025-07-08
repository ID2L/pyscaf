import logging

import pytest

from pyscaf.preference_chain import CircularDependencyError, best_execution_order
from pyscaf.preference_chain.model import Node

logger = logging.getLogger(__name__)


class TestBestExecutionOrder:
    """Test the best_execution_order function directly with the expected input format."""

    def test_simple_linear_execution_order(self):
        """Test simple linear dependency chain using the API format."""
        nodes = [
            Node(id="A", depends=[], after=None),
            Node(id="B", depends=["A"], after="A"),
            Node(id="C", depends=["B"], after="B"),
        ]

        result = best_execution_order(nodes)
        expected = ["A", "B", "C"]

        assert result == expected, f"Expected {expected}, got {result}"

    def test_diamond_execution_order(self):
        """Test diamond dependency pattern."""
        nodes = [
            Node(id="A", depends=[], after=None),
            Node(id="B", depends=["A"], after="A"),
            Node(id="C", depends=["A"], after="A"),
            Node(id="D", depends=["B", "C"], after="B"),
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
            Node(id="root", depends=[], after=None),
            Node(id="setup", depends=["root"], after="root"),
            Node(id="build", depends=["setup"], after="setup"),
        ]

        result = best_execution_order(nodes)
        expected = ["root", "setup", "build"]

        assert result == expected, f"Expected {expected}, got {result}"

    def test_multiple_external_dependencies(self):
        """Test nodes with multiple external dependencies."""
        nodes = [
            Node(id="A", depends=[], after=None),
            Node(id="B", depends=[], after=None),
            Node(id="C", depends=["A", "B"], after="A"),
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
            Node(id="A", depends=["B"], after="B"),
            Node(id="B", depends=["C"], after="C"),
            Node(id="C", depends=["A"], after="A"),
        ]

        with pytest.raises(CircularDependencyError):
            best_execution_order(nodes)

    def test_complex_real_world_scenario(self):
        """Test a complex scenario resembling real CI/CD pipeline dependencies."""
        nodes = [
            Node(id="checkout", depends=[], after=None),
            Node(id="install-deps", depends=["checkout"], after="checkout"),
            Node(id="lint", depends=["install-deps"], after="install-deps"),
            Node(id="test", depends=["install-deps"], after="install-deps"),
            Node(id="build", depends=["lint", "test"], after="lint"),
            Node(id="docker-build", depends=["build"], after="build"),
            Node(id="deploy-staging", depends=["docker-build"], after="docker-build"),
            Node(id="e2e-tests", depends=["deploy-staging"], after="deploy-staging"),
            Node(id="deploy-prod", depends=["e2e-tests"], after="e2e-tests"),
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
        nodes = [Node(id="single", depends=[], after=None)]
        result = best_execution_order(nodes)
        assert result == ["single"], f"Expected ['single'], got {result}"

    def test_invalid_after_field(self):
        """Test that invalid 'after' field raises an error."""
        nodes = [
            Node(id="A", depends=[], after=None),
            Node(id="B", depends=["A"], after="C"),  # 'C' is not in depends
        ]

        with pytest.raises(
            ValueError, match="Node 'B' has 'after'='C' but it's not in depends"
        ):
            best_execution_order(nodes)

    def test_auto_after_for_single_dependency(self):
        """Test that 'after' is automatically set for single dependency."""
        nodes = [
            Node(id="A", depends=[], after=None),
            Node(id="B", depends=["A"], after=None),  # Should auto-set to "A"
        ]

        result = best_execution_order(nodes)
        expected = ["A", "B"]
        assert result == expected, f"Expected {expected}, got {result}"


if __name__ == "__main__":
    # Configure logging for debug mode
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(levelname)s %(name)s::%(funcName)s: \n    %(message)s",
    )

    # Run a simple test
    nodes = [
        Node(id="A", depends=[], after=None),
        Node(id="B", depends=["A"], after="A"),
        Node(id="C", depends=["B"], after="B"),
    ]

    result = best_execution_order(nodes)
    print(f"Best execution order: {result}")
