"""Smoke tests for pyscaf — validates plugin discovery and CLI wiring."""

from click.testing import CliRunner

from pyscaf.actions import discover_actions
from pyscaf.main import cli
from pyscaf_core import Action


def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "pyscaf" in result.output


def test_cli_version():
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "pyscaf version" in result.output


def test_cli_init_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["init", "--help"])
    assert result.exit_code == 0
    assert "--author" in result.output
    assert "--versionning" in result.output
    assert "--license" in result.output


def test_discover_actions_count():
    actions = discover_actions()
    assert len(actions) == 8
    for action_cls in actions:
        assert issubclass(action_cls, Action)
        assert action_cls is not Action
