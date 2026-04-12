"""Smoke tests for pyscaf — validates plugin discovery and CLI wiring."""

from click.testing import CliRunner
from pyscaf_core import Action

from pyscaf.actions import discover_actions
from pyscaf.main import cli


def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "pyscaf" in result.output


def test_discover_actions_count():
    actions = discover_actions()
    assert len(actions) == 8
    for action_cls in actions:
        assert issubclass(action_cls, Action)
        assert action_cls is not Action
