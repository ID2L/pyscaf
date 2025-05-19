"""
Tests for the interactive mode.
"""
import os
import shutil
from pathlib import Path
from typing import Generator
from unittest.mock import patch

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


def test_interactive_package_project() -> None:
    """Test interactive mode for package project."""
    # Mock user input
    with patch("questionary.checkbox") as mock_checkbox, \
         patch("questionary.text") as mock_text, \
         patch("questionary.confirm") as mock_confirm:
        
        # Configure mocks
        mock_checkbox.return_value = [ProjectType.PACKAGE]
        mock_text.return_value = "guilhem.heinrich@gmail.com"
        mock_confirm.side_effect = [False, True, False, False, True]  # No formats, Use Git, No CI, No Docker, Skip install
        
        # Get project config
        config = get_project_config("test-package")
        
        # Verify config
        assert config.project_name == "test-package"
        assert config.project_type == [ProjectType.PACKAGE]
        assert config.author == "guilhem.heinrich@gmail.com"
        assert config.formats is None
        assert config.use_git
        assert config.ci_options is None
        assert not config.docker
        assert config.interactive
        assert config.no_install


def test_interactive_notebook_project() -> None:
    """Test interactive mode for notebook project."""
    # Mock user input
    with patch("questionary.checkbox") as mock_checkbox, \
         patch("questionary.text") as mock_text, \
         patch("questionary.confirm") as mock_confirm:
        
        # Configure mocks
        mock_checkbox.side_effect = [
            [ProjectType.NOTEBOOK],  # Project type
            ["html", "pdf"],  # Output formats
        ]
        mock_text.return_value = "guilhem.heinrich@gmail.com"
        mock_confirm.side_effect = [True, False, True]  # Use Git, No CI, Skip install
        
        # Get project config
        config = get_project_config("test-notebook")
        
        # Verify config
        assert config.project_name == "test-notebook"
        assert config.project_type == [ProjectType.NOTEBOOK]
        assert config.author == "guilhem.heinrich@gmail.com"
        assert config.formats is not None
        assert len(config.formats) == 2
        assert config.use_git
        assert config.ci_options is None
        assert not config.docker
        assert config.interactive
        assert config.no_install


def test_interactive_mixed_project() -> None:
    """Test interactive mode for mixed project."""
    # Mock user input
    with patch("questionary.checkbox") as mock_checkbox, \
         patch("questionary.text") as mock_text, \
         patch("questionary.confirm") as mock_confirm:
        
        # Configure mocks
        mock_checkbox.side_effect = [
            [ProjectType.PACKAGE, ProjectType.NOTEBOOK],  # Project type
            ["html", "pdf"],  # Output formats
            ["github"],  # CI options
        ]
        mock_text.return_value = "guilhem.heinrich@gmail.com"
        mock_confirm.side_effect = [True, True, False]  # Use Git, Docker, Skip install
        
        # Get project config
        config = get_project_config("test-mixed")
        
        # Verify config
        assert config.project_name == "test-mixed"
        assert set(config.project_type) == {ProjectType.PACKAGE, ProjectType.NOTEBOOK}
        assert config.author == "guilhem.heinrich@gmail.com"
        assert config.formats is not None
        assert len(config.formats) == 2
        assert config.use_git
        assert config.ci_options is not None
        assert len(config.ci_options) == 1
        assert config.docker
        assert config.interactive
        assert not config.no_install 