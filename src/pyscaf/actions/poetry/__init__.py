"""
Poetry initialization actions.
"""
import os
import subprocess
from pathlib import Path
from typing import Dict, Optional

from rich.console import Console

from pyscaf.actions import Action, CLIOption

console = Console()


def get_local_git_author():
    """Get the author name from the local git config."""
    try:
        git_name = subprocess.check_output(
            ['git', 'config', 'user.name']).decode().strip()
        git_email = subprocess.check_output(
            ['git', 'config', 'user.email']).decode().strip()
        default_author = f"{git_name} <{git_email}>"
    except subprocess.CalledProcessError:
        default_author = ""
    return default_author


class PoetryAction(Action):
    """Action to initialize a project with Poetry."""

    depends = []  # Poetry is the root action
    run_preferably_after = None
    cli_options = [
        CLIOption(
            name="--author",
            type="str",
            help="Author name",
            prompt="Author ?",
            default=get_local_git_author
        ),

        # Add other global options here
    ]

    def __init__(self, project_path):
        super().__init__(project_path)

    def skeleton(self, context: dict) -> Dict[Path, Optional[str]]:
        """
        Define the filesystem skeleton for Poetry initialization.

        Returns:
            Dictionary mapping paths to content
        """
        project_name = context.get("project_name", "myproject")
        currated_projet_name = project_name.replace("-", "_")

        # Read Poetry documentation
        poetry_doc_path = Path(__file__).parent / "README.md"
        poetry_doc = (
            poetry_doc_path.read_text() if poetry_doc_path.exists() else ""
        )

        # Return skeleton dictionary
        return {
            Path("README.md"): (
                f"# {project_name}\n\nA Python project created with pyscaf\n\n"
                f"{poetry_doc}\n"
            ),
            Path(f"{currated_projet_name}"): None,  # Create directory
            Path(f"{currated_projet_name}/__init__.py"): (
                f'"""\n{project_name} package.\n"""\n\n'
                f'__version__ = "0.1.0"\n'
            ),
        }

    def init(self, context: dict) -> None:
        """
        Initialize Poetry after skeleton creation.

        This will run 'poetry init' in interactive mode, allowing user input.
        """
        console.print("[bold blue]Initializing poetry project...[/bold blue]")

        try:
            # Change to project directory
            os.chdir(self.project_path)

            # Use subprocess.call to pass control to the terminal
            result = subprocess.call(
                [
                    "poetry",
                    "init",
                    "--no-interaction",
                    "--author",
                    context.get("author", "")
                ],
                # No redirection,
                # allows full terminal interaction
                stdin=None,
                stdout=None,
                stderr=None
            )

            if result == 0:
                console.print(
                    "[bold green]Poetry initialization successful![/bold green]"
                )
            else:
                console.print(
                    f"[bold yellow]Poetry init exited with code {result}[/bold yellow]"
                )

        except FileNotFoundError:
            console.print(
                "[bold yellow]Poetry not found. Please install it first:"
                "[/bold yellow]"
            )
            console.print("https://python-poetry.org/docs/#installation")

    def install(self, context: dict) -> None:
        """
        Install dependencies with Poetry.

        This will run 'poetry install' to install all dependencies.
        """
        console.print(
            "[bold blue]Installing dependencies with Poetry...[/bold blue]")

        try:
            # Ensure we're in the right directory
            os.chdir(self.project_path)

            # Run poetry install
            console.print("[bold cyan]Running poetry install...[/bold cyan]")

            result = subprocess.call(
                [
                    "poetry",
                    "install"
                ],
                stdin=None,
                stdout=None,
                stderr=None
            )

            if result == 0:
                console.print(
                    "[bold green]Poetry dependencies installed successfully!"
                    "[/bold green]"
                )
            else:
                console.print(
                    f"[bold yellow]Poetry install exited with code {result}"
                    f"[/bold yellow]"
                )

        except FileNotFoundError:
            console.print(
                "[bold yellow]Poetry not found. Please install it first:"
                "[/bold yellow]"
            )
            console.print("https://python-poetry.org/docs/#installation")
