"""
Poetry initialization actions.
"""
import os
import subprocess
from pathlib import Path
from typing import Dict, Optional

from rich.console import Console

from pyscaf.actions import Action
from pyscaf.models import ProjectConfig

console = Console()


class PoetryAction(Action):
    """Action to initialize a project with Poetry."""
    
    def skeleton(self) -> Dict[Path, Optional[str]]:
        """
        Define the filesystem skeleton for Poetry initialization.
        
        Returns:
            Dictionary mapping paths to content
        """
        project_name = self.config.project_name
        
        # Create pyproject.toml content
        pyproject_content = f"""[tool.poetry]
name = "{project_name}"
version = "0.1.0"
description = "A Python project"
authors = ["Your Name <your.email@example.com>"]
readme = "README.md"
packages = [{{include = "{project_name}", from = "src"}}]

[tool.poetry.dependencies]
python = ">=3.10"

[build-system]
requires = ["poetry-core>=2.0.0,<3.0.0"]
build-backend = "poetry.core.masonry.api"
"""
        
        # Return skeleton dictionary
        return {
            # Path("pyproject.toml"): pyproject_content,
            # Path("README.md"): f"# {project_name}\n\nA Python project created with pyscaf\n",
            # Path(f"src/{project_name}"): None,  # Create directory
            # Path(f"src/{project_name}/__init__.py"): f'"""\n{project_name} package.\n"""\n\n__version__ = "0.1.0"\n',
        }
    
    def init(self) -> None:
        """
        Initialize Poetry after skeleton creation.
        
        This will run 'poetry init' in interactive mode, allowing user input.
        """
        console.print("[bold blue]Initializing poetry project...[/bold blue]")
        
        try:
            # Change to project directory
            os.chdir(self.project_path)
            
            # Run poetry init interactively
            console.print("[bold cyan]Starting interactive poetry init session...[/bold cyan]")
            
            # Use subprocess.call to pass control to the terminal
            result = subprocess.call(
                ["poetry", "init"],
                # No redirection, allowing full terminal interaction
                stdin=None,
                stdout=None,
                stderr=None,
            )
            
            if result == 0:
                console.print("[bold green]Poetry initialization successful![/bold green]")
            else:
                console.print(f"[bold yellow]Poetry init exited with code {result}[/bold yellow]")
            
        except FileNotFoundError:
            console.print("[bold yellow]Poetry not found. Please install it first:[/bold yellow]")
            console.print("https://python-poetry.org/docs/#installation") 