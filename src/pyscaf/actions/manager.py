"""
Project action manager module.
"""
from pathlib import Path
from typing import List, Union, Dict, Any

from rich.console import Console

from pyscaf.actions import Action
from pyscaf.actions import discover_actions
from pyscaf.preference_chain.topologic_tree import best_execution_order
console = Console()


class ActionManager:
    """Manager for all project actions."""
    
    def __init__(self, project_name: Union[str, Path], context: Dict[str, Any]):
        """
        Initialize the action manager.
        
        Args:
            project_name: Name of the project to create
            context: Project context
        """
        self.project_path = Path.cwd() / project_name
        console.print(f"[bold green]Project path: [/bold green]{self.project_path}")
        self.context = context
        self.actions: List[Action] = []
        
        # Determine which actions to include based on configuration
        self._determine_actions()
    
    def _determine_actions(self) -> None:
        """Determine which actions to include based on configuration."""
        # Discover all available Action classes
        action_classes = discover_actions()
        # Build dependency/preference dicts for preference_chain
        deps = []
        action_class_by_id = {}
        for action_cls in action_classes:
            action_id = action_cls.__name__.replace('Action', '').lower()
            deps.append({
                "id": action_id,
                "depends": getattr(action_cls, "depends", []),
                "after": getattr(action_cls, "run_preferably_after", None)
            })
            action_class_by_id[action_id] = action_cls
        # Determine best execution order
        order = best_execution_order([
            {
                "id": d["id"],
                "fullfilled": [d["id"]],
                "external": d["depends"] or []
            }
            for d in deps
        ])
        # Instantiate actions in the optimal order
        self.actions = [action_class_by_id[action_id](self.project_path) for action_id in order]
    
    def create_project(self) -> None:
        """Create the project structure and initialize it."""
        # Create project directory if it doesn't exist
        self.project_path.mkdir(parents=True, exist_ok=True)
        
        console.print(f"[bold green]Creating project at: [/bold green]{self.project_path}")
        
        # First pass: Create all skeletons
        for action in self.actions:
            action_name = action.__class__.__name__
            console.print(f"[bold blue]Creating skeleton for: [/bold blue]{action_name}")
            action.create_skeleton(self.context)
        
        # Second pass: Initialize all actions
        for action in self.actions:
            action_name = action.__class__.__name__
            console.print(f"[bold blue]Initializing: [/bold blue]{action_name}")
            action.init(self.context)
        
        # Third pass: Install dependencies if not skipped
        if not self.context.get("no_install", False):
            for action in self.actions:
                action_name = action.__class__.__name__
                console.print(f"[bold blue]Installing dependencies for: [/bold blue]{action_name}")
                action.install(self.context)
        else:
            console.print("[bold yellow]Skipping installation.[/bold yellow]")
            
        console.print("[bold green]Project creation complete![/bold green]") 