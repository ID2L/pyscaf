"""
Pixi initialization actions.
"""

import os
import subprocess
from pathlib import Path

import tomli
import tomli_w
from rich.console import Console

from pyscaf.actions import Action, CLIOption

console = Console()


def get_local_git_author():
    """Get the author name from the local git config."""
    try:
        git_name = subprocess.check_output(["git", "config", "user.name"]).decode().strip()
        git_email = subprocess.check_output(["git", "config", "user.email"]).decode().strip()
        default_author = f"{git_name} <{git_email}>"
    except subprocess.CalledProcessError:
        default_author = ""
    return default_author


class CoreAction(Action):
    """Action to initialize a project with Pixi."""

    depends = set()  # Pixi is the root action
    run_preferably_after = None
    cli_options = [
        CLIOption(
            name="--author",
            type="str",
            help="Author name",
            prompt="Who is the main author of this project ?",
            default=get_local_git_author,
        ),
        CLIOption(
            name="--package-name",
            type="str",
            help="Package name (valid python identifier)",
            prompt="What is the name of the main package ?",
            default=lambda: "myproject",  # Fallback, logic in skeleton/init
        ),
    ]

    def __init__(self, project_path):
        super().__init__(project_path)

    def skeleton(self, context: dict) -> dict[Path, str | None]:
        """
        Define the filesystem skeleton for Core initialization.

        Returns:
            Dictionary mapping paths to content
        """
        project_name = context.get("project_name", "myproject")
        package_name = context.get("package_name", project_name.replace("-", "_"))

        # Read Pixi documentation (placeholder or from a file if exists)
        pixi_doc_path = Path(__file__).parent / "README.md"
        pixi_doc = pixi_doc_path.read_text() if pixi_doc_path.exists() else ""

        # Add default ruff settings for VSCode
        vscode_settings_path = Path(__file__).parent / "default_settings.json"
        vscode_settings = vscode_settings_path.read_text() if vscode_settings_path.exists() else ""
        # Return skeleton dictionary
        skeleton = {
            Path("README.md"): (f"# {project_name}\n\nA Python project created with pyscaf\n\n{pixi_doc}\n"),
            Path(f"src/{package_name}/__init__.py"): (f'"""\n{project_name} package.\n"""\n\n__version__ = "0.0.0"\n'),
            Path(".vscode/settings.json"): vscode_settings if vscode_settings else None,
        }
        return skeleton

    def init(self, context: dict) -> None:
        """
        Initialize Core after skeleton creation.

        This will run 'pixi init --format pyproject' in non-interactive mode.
        """
        console.print("[bold blue]Initializing core project with Pixi...[/bold blue]")

        try:
            # Change to project directory
            os.chdir(self.project_path)

            # Use subprocess.call to pass control to the terminal
            result = subprocess.call(
                [
                    "pixi",
                    "init",
                    "--format",
                    "pyproject",
                ],
                stdin=None,
                stdout=None,
                stderr=None,
            )

            project_name = context.get("project_name", "myproject")
            package_name = context.get("package_name", project_name.replace("-", "_"))

            # Pixi init --format pyproject creates a pyproject.toml if not exists
            pyproject_path = Path("pyproject.toml")
            if pyproject_path.exists():
                with pyproject_path.open("rb") as f:
                    pyproject_data = tomli.load(f)
                try:
                    # Configure project metadata if needed or Pixi specific sections
                    if "project" in pyproject_data:
                        old_name = pyproject_data["project"].get("name", "")
                        pyproject_data["project"]["name"] = project_name
                        pyproject_data["project"]["version"] = "0.0.0"

                        # Update pixi pypi-dependencies key as well
                        if "tool" in pyproject_data and "pixi" in pyproject_data["tool"]:
                            pixi_tool = pyproject_data["tool"]["pixi"]
                            if "pypi-dependencies" in pixi_tool:
                                pypi_deps = pixi_tool["pypi-dependencies"]
                                # If old_name is in pypi-dependencies, rename it to project_name
                                if old_name and old_name in pypi_deps:
                                    pypi_deps[project_name] = pypi_deps.pop(old_name)
                                # If the key is still missing, add it
                                if project_name not in pypi_deps:
                                    pypi_deps[project_name] = {"path": ".", "editable": True}

                            # Ensure default environment exists
                            if "environments" not in pixi_tool:
                                pixi_tool["environments"] = {}
                            if "default" not in pixi_tool["environments"]:
                                pixi_tool["environments"]["default"] = {"features": [], "solve-group": "default"}

                        if "authors" not in pyproject_data["project"]:
                            author_info = context.get("author", "")
                            if author_info:
                                # Quick parse "Name <email>"
                                if "<" in author_info and ">" in author_info:
                                    name, email = author_info.split("<")
                                    email = email.strip(">")
                                    pyproject_data["project"]["authors"] = [{"name": name.strip(), "email": email}]
                                else:
                                    pyproject_data["project"]["authors"] = [{"name": author_info.strip()}]

                    # Ensure tool.hatch.build exists for default build backend if we want hatch
                    if "tool" not in pyproject_data:
                        pyproject_data["tool"] = {}
                    if "hatch" not in pyproject_data["tool"]:
                        pyproject_data["tool"]["hatch"] = {
                            "build": {"targets": {"wheel": {"packages": [f"src/{package_name}"]}}}
                        }

                    with pyproject_path.open("wb") as f:
                        f.write(tomli_w.dumps(pyproject_data).encode("utf-8"))
                    console.print(f"[bold green]Configured pyproject.toml for {project_name}[/bold green]")
                except Exception as e:
                    console.print(f"[bold yellow]Error updating pyproject.toml: {e}[/bold yellow]")
            else:
                console.print("[bold yellow]pyproject.toml not found after pixi init.[/bold yellow]")

            if result == 0:
                console.print("[bold green]Pixi initialization successful![/bold green]")
            else:
                console.print(f"[bold yellow]Pixi init exited with code {result}[/bold yellow]")

        except FileNotFoundError:
            console.print("[bold yellow]Pixi not found. Please install it first:[/bold yellow]")
            console.print("https://pixi.sh/install.sh")

    def install(self, context: dict) -> None:
        """
        Install dependencies with Pixi.

        This will run 'pixi install' to install all dependencies.
        """
        super().init(context)

        console.print("[bold blue]Installing dependencies with Pixi...[/bold blue]")
        try:
            # Ensure we're in the right directory
            os.chdir(self.project_path)

            # Run pixi install
            console.print("[bold cyan]Running pixi install...[/bold cyan]")
            result = subprocess.call(["pixi", "install"], stdin=None, stdout=None, stderr=None)

            if result == 0:
                console.print("[bold green]Pixi dependencies installed successfully![/bold green]")
            else:
                console.print(f"[bold yellow]Pixi install exited with code {result}[/bold yellow]")

        except FileNotFoundError:
            console.print("[bold yellow]Pixi not found. Please install it first:[/bold yellow]")
            console.print("https://pixi.sh/install.sh")
            return
