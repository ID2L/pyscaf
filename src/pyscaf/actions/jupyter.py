"""
Jupyter initialization actions.
"""
import os
import subprocess
from pathlib import Path
from typing import Dict, Optional

from rich.console import Console

from pyscaf.actions import Action
from pyscaf.models import ProjectConfig

console = Console()


class JupyterAction(Action):
    """Action to initialize Jupyter notebook support in a project."""
    
    def skeleton(self) -> Dict[Path, Optional[str]]:
        """
        Define the filesystem skeleton for Jupyter notebook support.
        
        Returns:
            Dictionary mapping paths to content
        """
        project_name = self.config.project_name
        
        # Create a README for notebooks
        notebook_readme = f"""# {project_name} - Notebooks

This directory contains Jupyter notebooks for the {project_name} project.

## Usage

To use these notebooks:

1. Ensure you have the development dependencies installed:
   ```
   poetry install
   ```

2. Launch Jupyter:
   ```
   poetry run jupyter notebook
   ```
"""
        
        # Create .gitignore for notebooks to ignore checkpoints
        gitignore_content = """# Jupyter Notebook
.ipynb_checkpoints
*/.ipynb_checkpoints/*

# IPython
profile_default/
ipython_config.py
"""
        
        # Create a sample notebook
 
        # Return skeleton dictionary
        return {
            Path("notebooks"): None,  # Create main notebook directory
            Path("notebooks/README.md"): notebook_readme,
            Path(".gitignore"): gitignore_content,  # Append Jupyter gitignore to root .gitignore
        }
    
    def init(self) -> None:
        """
        Initialize Jupyter notebook support after skeleton creation.
        
        This will add the necessary dependencies to pyproject.toml.
        """
        console.print("[bold blue]Initializing Jupyter notebook support...[/bold blue]")
        
        try:
            # Change to project directory
            os.chdir(self.project_path)
            
            # Add Jupyter dependencies to poetry dev group
            console.print("[bold cyan]Adding Jupyter dependencies to poetry dev group...[/bold cyan]")
            
            jupyter_deps = [
                "jupyter",
                "notebook",
                "nbconvert",
                "ipykernel",
                "matplotlib",
                "pandas",
            ]
            
            # First ensure the dev group exists
            result = subprocess.call(
                ["poetry", "add", "--group", "dev"],
                stdin=None,
                stdout=None,
                stderr=None,
            )
            
            # Add each dependency to the dev group
            for dep in jupyter_deps:
                result = subprocess.call(
                    ["poetry", "add", "--group", "dev", dep],
                    stdin=None,
                    stdout=None,
                    stderr=None,
                )
                
                if result == 0:
                    console.print(f"[bold green]Added {dep} to dev dependencies[/bold green]")
                else:
                    console.print(f"[bold yellow]Failed to add {dep} (exit code {result})[/bold yellow]")
            
            console.print("[bold green]Jupyter dependencies added to poetry.dev group![/bold green]")
            
        except FileNotFoundError:
            console.print("[bold yellow]Poetry not found. Please install it first:[/bold yellow]")
            console.print("https://python-poetry.org/docs/#installation")
    
    def install(self) -> None:
        """
        Set up the Jupyter kernel for the project.
        
        This will create a Jupyter kernel specific to this project.
        """
        console.print("[bold blue]Setting up Jupyter kernel for the project...[/bold blue]")
        
        try:
            # Ensure we're in the right directory
            os.chdir(self.project_path)
            
            # Create a Jupyter kernel for this project
            console.print("[bold cyan]Creating Jupyter kernel for this project...[/bold cyan]")
            
            project_name = self.config.project_name
            
            # Run the ipykernel installation via poetry
            result = subprocess.call(
                [
                    "poetry", "run", "python", "-m", "ipykernel", 
                    "install", "--user", "--name", project_name,
                    "--display-name", f"{project_name} (Poetry)"
                ],
                stdin=None,
                stdout=None,
                stderr=None,
            )
            
            if result == 0:
                console.print("[bold green]Jupyter kernel created successfully![/bold green]")
                console.print(f"[bold green]You can now use the '{project_name} (Poetry)' kernel in Jupyter.[/bold green]")
            else:
                console.print(f"[bold yellow]Jupyter kernel creation exited with code {result}[/bold yellow]")
            
        except FileNotFoundError:
            console.print("[bold yellow]Poetry or Jupyter not found. Make sure they are installed.[/bold yellow]")
            console.print("https://python-poetry.org/docs/#installation") 