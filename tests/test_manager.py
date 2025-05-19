"""
Tests for the action manager.
"""
import os
import shutil
from pathlib import Path
from typing import Generator

import pytest

from pyscaf.actions.manager import ActionManager
from pyscaf.models import ProjectConfig, ProjectType


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


def test_manager_package_project(temp_project_dir: Path) -> None:
    """Test action manager with a package project."""
    config = ProjectConfig(
        project_name="test-package",
        project_type=[ProjectType.PACKAGE],
        use_git=True,
        interactive=False,
        no_install=True,
    )
    
    manager = ActionManager("test-package", config)
    manager.create_project()
    
    # Check project structure
    project_dir = temp_project_dir / "test-package"
    assert project_dir.exists()
    assert (project_dir / "test_package").exists()
    assert (project_dir / "test_package" / "__init__.py").exists()
    assert (project_dir / "pyproject.toml").exists()
    assert (project_dir / ".git").exists()
    assert (project_dir / ".gitignore").exists()


def test_manager_notebook_project(temp_project_dir: Path) -> None:
    """Test action manager with a notebook project."""
    config = ProjectConfig(
        project_name="test-notebook",
        project_type=[ProjectType.NOTEBOOK],
        use_git=True,
        interactive=False,
        no_install=True,
    )
    
    manager = ActionManager("test-notebook", config)
    manager.create_project()
    
    # Check project structure
    project_dir = temp_project_dir / "test-notebook"
    assert project_dir.exists()
    assert (project_dir / "notebooks").exists()
    assert (project_dir / "notebooks" / "README.md").exists()
    assert (project_dir / "pyproject.toml").exists()
    assert (project_dir / ".git").exists()
    assert (project_dir / ".gitignore").exists()


def test_manager_mixed_project(temp_project_dir: Path) -> None:
    """Test action manager with a mixed project (package + notebook)."""
    config = ProjectConfig(
        project_name="test-mixed",
        project_type=[ProjectType.PACKAGE, ProjectType.NOTEBOOK],
        use_git=True,
        interactive=False,
        no_install=True,
    )
    
    manager = ActionManager("test-mixed", config)
    manager.create_project()
    
    # Check project structure
    project_dir = temp_project_dir / "test-mixed"
    assert project_dir.exists()
    assert (project_dir / "test_mixed").exists()
    assert (project_dir / "test_mixed" / "__init__.py").exists()
    assert (project_dir / "notebooks").exists()
    assert (project_dir / "notebooks" / "README.md").exists()
    assert (project_dir / "pyproject.toml").exists()
    assert (project_dir / ".git").exists()
    assert (project_dir / ".gitignore").exists()


def test_manager_no_git(temp_project_dir: Path) -> None:
    """Test action manager without Git."""
    config = ProjectConfig(
        project_name="test-no-git",
        project_type=[ProjectType.PACKAGE],
        use_git=False,
        interactive=False,
        no_install=True,
    )
    
    manager = ActionManager("test-no-git", config)
    manager.create_project()
    
    # Check project structure
    project_dir = temp_project_dir / "test-no-git"
    assert project_dir.exists()
    assert (project_dir / "test_no_git").exists()
    assert (project_dir / "test_no_git" / "__init__.py").exists()
    assert (project_dir / "pyproject.toml").exists()
    assert not (project_dir / ".git").exists() 