"""
Tests for the interactive mode.
"""
import os
import shutil
from pathlib import Path
from typing import Generator
from unittest.mock import patch, MagicMock

import pytest

from pyscaf.interactive import get_project_config
from pyscaf.models import ProjectType


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


@patch("pyscaf.interactive.questionary.checkbox")
@patch("pyscaf.interactive.questionary.text")
@patch("pyscaf.interactive.questionary.confirm")
def test_interactive_package_project(
    mock_confirm,
    mock_text,
    mock_checkbox,
) -> None:
    """Test interactive mode for package project."""
    # Create mock objects
    checkbox_mock = MagicMock()
    checkbox_mock.ask.return_value = [ProjectType.PACKAGE]
    mock_checkbox.return_value = checkbox_mock

    text_mock = MagicMock()
    text_mock.ask.return_value = "guilhem.heinrich@gmail.com"
    mock_text.return_value = text_mock

    confirm_mock = MagicMock()
    confirm_mock.ask.side_effect = [True, False, True]  # [use_git, docker, no_install]
    mock_confirm.return_value = confirm_mock
        
    # Get project config
    config = get_project_config("test-package")
    
    # Verify config
    assert config.project_name == "test-package"
    assert config.project_type == [ProjectType.PACKAGE]
    assert config.author == "guilhem.heinrich@gmail.com"
    assert config.formats is None  # Formats not available for package
    assert config.use_git
    assert config.ci_options is None  # CI options not available
    assert not config.docker
    assert config.interactive
    assert config.no_install


@patch("pyscaf.interactive.questionary.checkbox")
@patch("pyscaf.interactive.questionary.text")
@patch("pyscaf.interactive.questionary.confirm")
def test_interactive_notebook_project(
    mock_confirm,
    mock_text,
    mock_checkbox,
) -> None:
    """Test interactive mode for notebook project."""
    # Create mock objects
    checkbox_mock = MagicMock()
    checkbox_mock.ask.side_effect = [
        [ProjectType.NOTEBOOK],  # Project type
        ["html", "pdf"],  # Output formats
    ]
    mock_checkbox.return_value = checkbox_mock

    text_mock = MagicMock()
    text_mock.ask.return_value = "guilhem.heinrich@gmail.com"
    mock_text.return_value = text_mock

    confirm_mock = MagicMock()
    confirm_mock.ask.side_effect = [True, False, True]  # [use_git, docker, no_install]
    mock_confirm.return_value = confirm_mock
        
    # Get project config
    config = get_project_config("test-notebook")
    
    # Verify config
    assert config.project_name == "test-notebook"
    assert config.project_type == [ProjectType.NOTEBOOK]
    assert config.author == "guilhem.heinrich@gmail.com"
    assert config.formats is not None
    assert len(config.formats) == 2
    assert config.use_git
    assert config.ci_options is None  # CI options not available
    assert not config.docker
    assert config.interactive
    assert config.no_install


@patch("pyscaf.interactive.questionary.checkbox")
@patch("pyscaf.interactive.questionary.text")
@patch("pyscaf.interactive.questionary.confirm")
def test_interactive_mixed_project(
    mock_confirm,
    mock_text,
    mock_checkbox,
) -> None:
    """Test interactive mode for mixed project."""
    # Create mock objects
    checkbox_mock = MagicMock()
    checkbox_mock.ask.side_effect = [
        [ProjectType.PACKAGE, ProjectType.NOTEBOOK],  # Project type
        ["html", "pdf"],  # Output formats
    ]
    mock_checkbox.return_value = checkbox_mock

    text_mock = MagicMock()
    text_mock.ask.return_value = "guilhem.heinrich@gmail.com"
    mock_text.return_value = text_mock

    confirm_mock = MagicMock()
    confirm_mock.ask.side_effect = [True, True, False]  # [use_git, docker, no_install]
    mock_confirm.return_value = confirm_mock
        
    # Get project config
    config = get_project_config("test-mixed")
    
    # Verify config
    assert config.project_name == "test-mixed"
    assert set(config.project_type) == {ProjectType.PACKAGE, ProjectType.NOTEBOOK}
    assert config.author == "guilhem.heinrich@gmail.com"
    assert config.formats is not None
    assert len(config.formats) == 2
    assert config.use_git
    assert config.ci_options is None  # CI options not available (commented in code)
    assert config.docker
    assert config.interactive
    assert not config.no_install 