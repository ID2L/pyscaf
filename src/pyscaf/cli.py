"""
Command-line interface for pyscaf.
"""
import sys
from typing import List, Optional

import click
from rich.console import Console

from pyscaf import __version__
from pyscaf.actions.manager import ActionManager
from pyscaf.models import (
    CIOption,
    OutputFormat,
    ProjectConfig,
    ProjectType,
    
)
from pyscaf.interactive import get_project_config

console = Console()


def print_version(ctx, param, value):
    """Print version and exit."""
    if not value or ctx.resilient_parsing:
        return
    console.print(f"pyscaf version {__version__}")
    ctx.exit()


class CustomCommand(click.Command):
    """Custom command class to make type option conditionally required."""
    def parse_args(self, ctx, args):
        # Parse once to check for --interactive option
        parser = self.make_parser(ctx)
        opts, _, param_order = parser.parse_args(args=list(args))
        interactive_present = opts.get('interactive', False)
        
        # Modify required options based on interactive mode
        for param in self.get_params(ctx):
            if param.name == 'type' and interactive_present:
                param.required = False
                
        return super().parse_args(ctx, args)


@click.group()
@click.version_option(
    __version__, "--version", "-V", callback=print_version, help="Show the version and exit."
)
def cli():
    """🧪 pyscaf - Project generator for laboratory, teaching and data analysis."""
    pass


@cli.command(cls=CustomCommand)
@click.argument("project_name")
@click.option(
    "--type", "-t",
    type=click.Choice([t.value for t in ProjectType], case_sensitive=False),
    required=True,
    multiple=True,
    help="Type of project to generate."
)
@click.option(
    "--formats",
    type=click.Choice([f.value for f in OutputFormat], case_sensitive=False),
    multiple=True,
    help="Desired output formats (multiple selections possible)."
)
@click.option(
    "--git/--no-git",
    default=False,
    show_default=True,
    help="Initialize Git repository."
)
@click.option(
    "--remote-url",
    type=str,
    help="Remote repository URL for Git versioning."
)
@click.option(
    "--ci",
    type=click.Choice([c.value for c in CIOption], case_sensitive=False),
    multiple=True,
    help="Add CI/CD workflows (multiple selections possible)."
)
@click.option(
    "--docker/--no-docker",
    default=False,
    show_default=True,
    help="Include a Dockerfile for reproducible environment."
)
@click.option(
    "--interactive",
    is_flag=True,
    help="Enable interactive mode (asks questions to the user)."
)
@click.option(
    "--no-install",
    is_flag=True,
    help="Skip installation step."
)
def init(
    project_name: str,
    type: Optional[List[str]] = None,
    formats: Optional[List[str]] = None,
    git: bool = False,
    remote_url: Optional[str] = None,
    ci: Optional[List[str]] = None,
    docker: bool = False,
    interactive: bool = False,
    no_install: bool = False,
):
    """
    Initialize a new customized project structure with Python, Jupyter,
    Quarto Bookdown, Web App, CI/CD, Docker, and more.
    """
    config = None

    if interactive:
        config = get_project_config(project_name)
    else:
        # Check if type is provided when not in interactive mode
        if type is None:
            console.print("[bold red]Error:[/bold red] The --type option is required in non-interactive mode.")
            sys.exit(1)
            
        # Convert string values to enum types
        project_type = [ProjectType(p) for p in type]
        output_formats = [OutputFormat(f) for f in formats] if formats else None
        ci_options = [CIOption(c) for c in ci] if ci else None

        # Create configuration
        config = ProjectConfig(
            project_name=project_name,
            project_type=project_type,
            formats=output_formats,
            use_git=git,
            remote_url=remote_url,
            ci_options=ci_options,
            docker=docker,
            interactive=interactive,
            no_install=no_install,
        )

    console.print(f"[bold green]Project configuration:[/bold green]")
    console.print(f"Project name: [bold]{config.project_name}[/bold]")
    console.print(f"Project type: [bold]{', '.join(f.value for f in config.project_type)}[/bold]")
    if config.formats:
        console.print(f"Output formats: [bold]{', '.join(f.value for f in config.formats)}[/bold]")
    console.print(f"Git: [bold]{'Yes' if config.use_git else 'No'}[/bold]")
    if config.ci_options:
        console.print(f"CI/CD options: [bold]{', '.join(c.value for c in config.ci_options)}[/bold]")
    console.print(f"Docker: [bold]{'Yes' if config.docker else 'No'}[/bold]")
    console.print(f"Interactive mode: [bold]{'Yes' if config.interactive else 'No'}[/bold]")

    # Create the project using ActionManager
    manager = ActionManager(project_name, config)
    manager.create_project()


def main():
    """Entry point for the CLI."""
    try:
        cli()
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main() 