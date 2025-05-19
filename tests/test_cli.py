"""
Tests for the CLI functionality.
"""
import os
import shutil
from pathlib import Path
from typing import Generator

import pytest
from click.testing import CliRunner

from pyscaf.cli import cli
from pyscaf.models import ProjectType, VersioningSystem


@pytest.fixture
def runner() -> CliRunner:
    """Create a CLI runner for testing."""
    return CliRunner()


@pytest.fixture
def temp_project_dir(tmp_path: Path) -> Generator[Path, None, None]:
    """Create a temporary directory for project testing."""
    # Change to temporary directory
    original_dir = os.getcwd()
    os.chdir(tmp_path)
    
    yield tmp_path
    
    # Cleanup
    os.chdir(original_dir)
    shutil.rmtree(tmp_path)


def test_cli_version(runner: CliRunner) -> None:
    """Test the version command."""
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "pyscaf version" in result.output


def test_cli_init_package(runner: CliRunner, temp_project_dir: Path) -> None:
    """Test initializing a package project."""
    result = runner.invoke(
        cli,
        [
            "init",
            "test-package",
            "--type",
            ProjectType.PACKAGE.value,
            "--versioning",
            VersioningSystem.GITHUB.value,
            "--no-install",
        ],
    )
    
    assert result.exit_code == 0
    
    # Check project structure
    project_dir = temp_project_dir / "test-package"
    assert project_dir.exists()
    assert (project_dir / "test_package").exists()
    assert (project_dir / "test_package" / "__init__.py").exists()
    assert (project_dir / "pyproject.toml").exists()
    assert (project_dir / ".git").exists()
    assert (project_dir / ".gitignore").exists()


def test_cli_init_notebook(runner: CliRunner, temp_project_dir: Path) -> None:
    """Test initializing a notebook project."""
    result = runner.invoke(
        cli,
        [
            "init",
            "test-notebook",
            "--type",
            ProjectType.NOTEBOOK.value,
            "--versioning",
            VersioningSystem.GITHUB.value,
            "--no-install",
        ],
    )
    
    assert result.exit_code == 0
    
    # Check project structure
    project_dir = temp_project_dir / "test-notebook"
    assert project_dir.exists()
    assert (project_dir / "notebooks").exists()
    assert (project_dir / "notebooks" / "README.md").exists()
    assert (project_dir / "pyproject.toml").exists()
    assert (project_dir / ".git").exists()
    assert (project_dir / ".gitignore").exists()


def test_cli_init_interactive(runner: CliRunner, temp_project_dir: Path) -> None:
    """Test interactive project initialization."""
    # Simulate user input for interactive mode
    result = runner.invoke(
        cli,
        ["init", "test-interactive", "--interactive"],
        input="\n".join([
            "package",  # Select package type
            "guilhem.heinrich@gmail.com",  # Author
            "n",  # No output formats
            "git",  # Versioning system
            "n",  # No CI options
            "n",  # No Docker
            "y",  # Skip installation
        ]),
    )
    
    assert result.exit_code == 0
    
    # Check project structure
    project_dir = temp_project_dir / "test-interactive"
    assert project_dir.exists()
    assert (project_dir / "test_interactive").exists()
    assert (project_dir / "test_interactive" / "__init__.py").exists()
    assert (project_dir / "pyproject.toml").exists()
    assert (project_dir / ".git").exists()
    assert (project_dir / ".gitignore").exists()


def test_cli_init_invalid_type(runner: CliRunner, temp_project_dir: Path) -> None:
    """Test initialization with invalid project type."""
    result = runner.invoke(
        cli,
        [
            "init",
            "test-invalid",
            "--type",
            "invalid-type",
        ],
    )
    
    assert result.exit_code != 0
    assert "Invalid value for '--type'" in result.output 