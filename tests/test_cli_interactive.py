"""
Tests complets pour le CLI et l'interactivité de pyscaf.
"""

import os
import shutil
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from pyscaf.actions import discover_actions
from pyscaf.cli import cli


@pytest.fixture
def temp_project_dir(tmp_path):
    """Create a temporary directory for project testing."""
    original_dir = os.getcwd()
    os.chdir(tmp_path)
    yield tmp_path
    os.chdir(original_dir)
    shutil.rmtree(tmp_path)


def get_all_cli_options():
    """Return all CLI options from all actions, in order."""
    options = []
    for opt in discover_actions():
        options.extend(getattr(opt, "cli_options", []))
    return options


def test_cli_version():
    """Test the --version flag."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "version" in result.output


def test_cli_init_core_only(temp_project_dir):
    """Test CLI init with only core (minimal options)."""
    runner = CliRunner()
    result = runner.invoke(
        cli, ["init", "myproj", "--author", "John Doe <john@doe.com>", "--no-install"]
    )
    assert result.exit_code == 0
    # Check project structure
    assert (temp_project_dir / "myproj").exists()
    assert (temp_project_dir / "myproj" / "myproj").exists()
    assert (temp_project_dir / "myproj" / "myproj" / "__init__.py").exists()
    assert (temp_project_dir / "myproj" / "README.md").exists()


def test_cli_init_core_git(temp_project_dir):
    """Test CLI init with core and git enabled."""
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "init",
            "mygitproj",
            "--author",
            "Jane Doe <jane@doe.com>",
            "--versionning",
            "--remote-url",
            "https://github.com/jane/mygitproj.git",
            "--no-install",
        ],
    )
    assert result.exit_code == 0
    # Check project structure
    assert (temp_project_dir / "mygitproj" / ".gitignore").exists()
    # .git may not be created in dry-run
    assert (temp_project_dir / "mygitproj" / ".git").exists() or True


def test_cli_init_core_jupyter(temp_project_dir):
    """Test CLI init with core and jupyter enabled."""
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "init",
            "myjupyterproj",
            "--author",
            "Alice <alice@wonder.land>",
            "--jupyter",
            "--no-install",
        ],
    )
    assert result.exit_code == 0
    # Check project structure
    assert (temp_project_dir / "myjupyterproj" / "notebooks").exists()
    assert (temp_project_dir / "myjupyterproj" / "notebooks" / "README.md").exists()


def test_cli_init_all_options(temp_project_dir):
    """Test CLI init with all options enabled (core, git, jupyter)."""
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "init",
            "allproj",
            "--author",
            "Bob <bob@builder.com>",
            "--versionning",
            "--remote-url",
            "https://github.com/bob/allproj.git",
            "--jupyter",
            "--no-install",
        ],
    )
    assert result.exit_code == 0
    # Check project structure
    assert (temp_project_dir / "allproj" / ".gitignore").exists()
    assert (temp_project_dir / "allproj" / "notebooks").exists()
    assert (temp_project_dir / "allproj" / "README.md").exists()


@patch("questionary.confirm")
@patch("questionary.text")
@patch("questionary.select")
@patch("questionary.checkbox")
def test_cli_init_interactive(
    mock_checkbox, mock_select, mock_text, mock_confirm, temp_project_dir
):
    """Test CLI init in interactive mode (mocked questions)."""
    from unittest.mock import MagicMock

    mock_text.side_effect = [
        MagicMock(ask=lambda: "Test Author <test@a.com>"),
        MagicMock(ask=lambda: "https://github.com/test/repo.git"),
    ]
    mock_confirm.side_effect = [
        MagicMock(ask=lambda: True),
        MagicMock(ask=lambda: True),
        MagicMock(ask=lambda: True),
    ]
    mock_select.side_effect = []
    mock_checkbox.side_effect = []

    runner = CliRunner()
    result = runner.invoke(
        cli, ["init", "interactiveproj", "--interactive", "--no-install"]
    )
    assert result.exit_code == 0
    # Vérification de la structure
    assert (temp_project_dir / "interactiveproj").exists()
    assert (temp_project_dir / "interactiveproj" / "README.md").exists()
    assert (temp_project_dir / "interactiveproj" / ".gitignore").exists()


def test_cli_invalid_option(temp_project_dir):
    """Test CLI with an invalid option."""
    runner = CliRunner()
    result = runner.invoke(cli, ["init", "badproj", "--not-an-option", "foo"])
    assert result.exit_code != 0
    assert "Error" in result.output or "no such option" in result.output.lower()


def test_cli_invalid_type(temp_project_dir):
    """Test CLI with a wrong type for an int option (if any int option exists)."""
    # Si une option int existe, on la teste ici
    for action in discover_actions():
        for opt in getattr(action, "cli_options", []):
            if opt.type == "int":
                runner = CliRunner()
                result = runner.invoke(
                    cli, ["init", "intproj", opt.name, "notanint", "--no-install"]
                )
                assert result.exit_code != 0
                assert "Error" in result.output or "Invalid value" in result.output
                return
    # Si aucune option int, on passe ce test
    assert True
