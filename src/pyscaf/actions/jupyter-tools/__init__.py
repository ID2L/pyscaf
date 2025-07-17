"""
jupyter tools initialization actions.
"""

import os
import subprocess
from pathlib import Path
from typing import Dict, Optional

import tomli
import tomli_w
from rich.console import Console

from pyscaf.actions import Action, CLIOption

console = Console()


class JupyterToolsAction(Action):
    """Action to provide Jupyter notebook manipulation tools."""

    depends = {"jupyter"}
    run_preferably_after = "jupyter"
    cli_options = [
        CLIOption(
            name="--jupyter-tools",
            type="bool",
            help="Add Jupyter notebook manipulation tools",
            prompt="Do you want to add Jupyter notebook manipulation tools ?",
            default=True,
        ),
    ]

    def __init__(self, project_path):
        super().__init__(project_path)

    def activate(self, context: dict) -> bool:
        return context.get("jupyter_tools") is None or context.get(
            "jupyter_tools", True
        )

    def skeleton(self, context: dict) -> Dict[Path, Optional[str]]:
        """
        Define the filesystem skeleton for Jupyter tools.

        Returns:
            Dictionary mapping paths to content
        """

        # Read configuration file
        config_path = Path(__file__).parent / "config.toml"
        readme_path = Path(__file__).parent / "README.md"
        readme_content = readme_path.read_text() if readme_path.exists() else ""
        config_content = config_path.read_text() if config_path.exists() else ""

        # Parse config.toml to get directory paths
        config_dirs = []
        if config_path.exists():
            try:
                config_data = tomli.loads(config_content)
                if (
                    "tool" in config_data
                    and "pyscaf" in config_data["tool"]
                    and "jupyter-tools" in config_data["tool"]["pyscaf"]
                ):
                    jupyter_tools_config = config_data["tool"]["pyscaf"][
                        "jupyter-tools"
                    ]
                    # Extract all directory paths from the config
                    for key, value in jupyter_tools_config.items():
                        if isinstance(value, str) and (
                            "dir" in key or "directory" in key
                        ):
                            config_dirs.append(Path(value))
            except Exception as e:
                console.print(
                    f"[bold yellow]Warning: Could not parse config.toml: {e}[/bold yellow]"
                )

        # Create tools directory structure with embedded documentation

        # Copy scripts from the source
        scripts_dir = Path(__file__).parent / "scripts"

        skeleton = {
            Path("jupyter_tools"): None,  # Create tools directory
            Path("README.md"): readme_content,  # Add to configuration
            Path("pyproject.toml"): config_content,
        }

        # Add configured directories to skeleton
        for dir_path in config_dirs:
            skeleton[dir_path] = None  # Create directory

        # Add all script files
        if scripts_dir.exists():
            for script_file in scripts_dir.glob("*.py"):
                script_content = script_file.read_text()
                skeleton[Path(f"jupyter_tools/{script_file.name}")] = script_content

        return skeleton

    def init(self, context: dict) -> None:
        """
        Initialize Jupyter tools after skeleton creation.

        This will add the necessary dependencies to pyproject.toml and register CLI scripts in [project][scripts].
        """
        console.print("[bold blue]Initializing Jupyter tools...[/bold blue]")

        try:
            # Change to project directory
            os.chdir(self.project_path)

            # Add Jupyter tools dependencies to poetry dev group
            console.print(
                "[bold cyan]Adding Jupyter tools dependencies to poetry dev group...[/bold cyan]"
            )

            jupyter_tools_deps = [
                "jupytext",
                "nbconvert",
                "weasyprint",
                "pandoc",
            ]

            # Read current pyproject.toml
            pyproject_path = Path("pyproject.toml")
            with open(pyproject_path, "rb") as f:
                pyproject = tomli.load(f)

            # Ensure tool.poetry.group.dev exists
            if "tool" not in pyproject:
                pyproject["tool"] = {}
            if "poetry" not in pyproject["tool"]:
                pyproject["tool"]["poetry"] = {}
            if "group" not in pyproject["tool"]["poetry"]:
                pyproject["tool"]["poetry"]["group"] = {}
            if "dev" not in pyproject["tool"]["poetry"]["group"]:
                pyproject["tool"]["poetry"]["group"]["dev"] = {"dependencies": {}}

            # Add each dependency to the dev group
            for dep in jupyter_tools_deps:
                pyproject["tool"]["poetry"]["group"]["dev"]["dependencies"][dep] = "*"
                console.print(
                    f"[bold green]Added {dep} to dev dependencies[/bold green]"
                )

            # Ensure project.scripts exists
            if "project" not in pyproject:
                pyproject["project"] = {}
            if "scripts" not in pyproject["project"]:
                pyproject["project"]["scripts"] = {}
            scripts = pyproject["project"]["scripts"]

            # Register the scripts (user must provide arguments manually)
            scripts["py-to-nb"] = "jupyter_tools.py_to_notebook:main"
            scripts["exec-nb"] = "jupyter_tools.execute_notebook:main"
            scripts["nb-to-html"] = "jupyter_tools.notebook_to_html:main"

            # Write back to pyproject.toml
            with open(pyproject_path, "wb") as f:
                tomli_w.dump(pyproject, f)

            console.print(
                "[bold green]Jupyter tools dependencies and scripts added to pyproject.toml ([project][scripts])![/bold green]"
            )
            console.print(
                "[bold blue]You can now use the scripts via poetry run py-to-nb, exec-nb, nb-to-html (arguments required).[/bold blue]"
            )

        except FileNotFoundError:
            console.print(
                "[bold yellow]pyproject.toml not found. Please ensure you are in a Poetry project.[/bold yellow]"
            )

    def install(self, context: dict) -> None:
        """
        Set up the Jupyter tools for the project.

        This will make the tools executable and create convenience scripts.
        """
        console.print("[bold blue]Setting up Jupyter tools...[/bold blue]")

        try:
            # Ensure we're in the right directory
            os.chdir(self.project_path)

            # Make tools executable (on Unix-like systems)
            tools_dir = Path("tools")
            if tools_dir.exists():
                for script_file in tools_dir.glob("*.py"):
                    try:
                        # Make executable on Unix-like systems
                        script_file.chmod(0o755)
                        console.print(
                            f"[bold green]Made {script_file.name} executable[/bold green]"
                        )
                    except OSError:
                        # On Windows, this will fail but that's okay
                        pass

            console.print("[bold green]Jupyter tools setup complete![/bold green]")
            console.print(
                "[bold blue]You can now use the tools in the tools/ directory.[/bold blue]"
            )

        except Exception as e:
            console.print(
                f"[bold yellow]Error setting up Jupyter tools: {e}[/bold yellow]"
            )
