"""
Project action manager module.
"""
from pathlib import Path
from typing import List, Union

from rich.console import Console

from pyscaf.actions import Action
from pyscaf.actions.poetry import PoetryAction
from pyscaf.actions.jupyter import JupyterAction
from pyscaf.actions.git import GitAction
from pyscaf.models import ProjectConfig, ProjectType, VersioningSystem

console = Console()


class ActionManager:
    """Manager for all project actions."""
    
    def __init__(self, project_name: Union[str, Path], config: ProjectConfig):
        """
        Initialize the action manager.
        
        Args:
            project_name: Name of the project to create
            config: Project configuration
        """
        self.project_path = Path.cwd() / project_name
        console.print(f"[bold green]Project path: [/bold green]{self.project_path}")
        self.config = config
        self.actions: List[Action] = []
        
        # Determine which actions to include based on configuration
        self._determine_actions()
    
    def _determine_actions(self) -> None:
        """Determine which actions to include based on configuration."""
        self.actions.append(PoetryAction(self.project_path, self.config))
        
        # Add JupyterAction if NOTEBOOK type is selected
        if ProjectType.NOTEBOOK in self.config.project_type:
            console.print("[bold blue]Adding Jupyter notebook support...[/bold blue]")
            self.actions.append(JupyterAction(self.project_path, self.config))
        
        # Add GitAction if versioning is enabled
        if self.config.versioning != VersioningSystem.NONE:
            console.print(f"[bold blue]Adding Git support with {self.config.versioning.value}...[/bold blue]")
            self.actions.append(GitAction(self.project_path, self.config))
        
        # Other actions would be added here based on config
        
    def create_project(self) -> None:
        """Create the project structure and initialize it."""
        # Create project directory if it doesn't exist
        self.project_path.mkdir(parents=True, exist_ok=True)
        
        console.print(f"[bold green]Creating project at: [/bold green]{self.project_path}")
        
        # First pass: Create all skeletons
        for action in self.actions:
            action_name = action.__class__.__name__
            console.print(f"[bold blue]Creating skeleton for: [/bold blue]{action_name}")
            action.create_skeleton()
        
        # Second pass: Initialize all actions
        for action in self.actions:
            action_name = action.__class__.__name__
            console.print(f"[bold blue]Initializing: [/bold blue]{action_name}")
            action.init()
        
        # Third pass: Install dependencies
        for action in self.actions:
            action_name = action.__class__.__name__
            console.print(f"[bold blue]Installing dependencies for: [/bold blue]{action_name}")
            action.install()
            
        console.print("[bold green]Project creation complete![/bold green]") 