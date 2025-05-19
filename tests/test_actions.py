"""
Tests for the action classes.
"""
import os
import shutil
from pathlib import Path
from typing import Generator

import pytest

from pyscaf.actions import Action
from pyscaf.actions.poetry import PoetryAction
from pyscaf.actions.git import GitAction
from pyscaf.actions.jupyter import JupyterAction
from pyscaf.models import ProjectConfig, ProjectType, VersioningSystem


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


@pytest.fixture
def project_config() -> ProjectConfig:
    """Create a test project configuration."""
    return ProjectConfig(
        project_name="test-project",
        project_type=[ProjectType.PACKAGE],
        versioning=VersioningSystem.GITHUB,
        interactive=False,
        no_install=True,
    )


def test_poetry_action(temp_project_dir: Path, project_config: ProjectConfig) -> None:
    """Test Poetry action."""
    action = PoetryAction(temp_project_dir, project_config)
    
    # Test skeleton creation
    created_paths = action.create_skeleton()
    assert len(created_paths) > 0
    
    # Check created files
    assert (temp_project_dir / "test_project").exists()
    assert (temp_project_dir / "test_project" / "__init__.py").exists()
    assert (temp_project_dir / "README.md").exists()
    
    # Test init (should not fail)
    action.init()
    
    # Test install (should not fail)
    action.install()


def test_git_action(temp_project_dir: Path, project_config: ProjectConfig) -> None:
    """Test Git action."""
    action = GitAction(temp_project_dir, project_config)
    
    # Test skeleton creation
    created_paths = action.create_skeleton()
    assert len(created_paths) > 0
    
    # Check created files
    assert (temp_project_dir / ".gitignore").exists()
    
    # Test init (should not fail)
    action.init()
    
    # Check if .git directory exists
    assert (temp_project_dir / ".git").exists()


def test_jupyter_action(temp_project_dir: Path, project_config: ProjectConfig) -> None:
    """Test Jupyter action."""
    # Modify config to include notebook type
    project_config.project_type.append(ProjectType.NOTEBOOK)
    
    action = JupyterAction(temp_project_dir, project_config)
    
    # Test skeleton creation
    created_paths = action.create_skeleton()
    assert len(created_paths) > 0
    
    # Check created files
    assert (temp_project_dir / "notebooks").exists()
    assert (temp_project_dir / "notebooks" / "README.md").exists()
    
    # Test init (should not fail)
    action.init()
    
    # Test install (should not fail)
    action.install()


def test_action_abstract_base() -> None:
    """Test that Action is an abstract base class."""
    with pytest.raises(TypeError):
        Action(Path("test"), ProjectConfig(
            project_name="test",
            project_type=[ProjectType.PACKAGE],
            versioning=VersioningSystem.NONE,
            interactive=False,
            no_install=True,
        )) 