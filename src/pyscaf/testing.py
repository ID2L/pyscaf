"""Testing configuration for pyscaf action tests."""

import importlib.resources
from pathlib import Path

from pyscaf_core.testing import ActionTestConfig

_YAML_DIR = Path(str(importlib.resources.files("pyscaf") / "action_test_yamls"))


def get_test_config() -> ActionTestConfig:
    return ActionTestConfig(yaml_dir=_YAML_DIR, cli_command="pyscaf")
