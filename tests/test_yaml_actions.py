"""YAML-driven action tests for pyscaf — powered by pyscaf_core.testing."""

from pyscaf_core.testing import create_yaml_tests

test_action = create_yaml_tests(entry_point_name="pyscaf")
