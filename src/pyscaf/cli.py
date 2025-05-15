"""
Command-line interface for pyscaf.
"""
import sys
from typing import List, Optional

import click
from rich.console import Console

from pyscaf import __version__
from pyscaf.models import (
    CIOption,
    OutputFormat,
    ProjectConfig,
    ProjectType,
    VersioningSystem,
)
from pyscaf.interactive import get_project_config

console = Console()


def print_version(ctx, param, value):
    """Print version and exit."""
    if not value or ctx.resilient_parsing:
        return
    console.print(f"pyscaf version {__version__}")
    ctx.exit()


@click.group()
@click.version_option(
    __version__, "--version", "-V", callback=print_version, help="Show the version and exit."
)
def cli():
    """🧪 pyscaf - Générateur de projet pour laboratoire, enseignement et analyse de données."""
    pass


@cli.command()
@click.argument("project_name")
@click.option(
    "--type", "-t",
    type=click.Choice([t.value for t in ProjectType], case_sensitive=False),
    required=True,
    multiple=True,
    help="Type de projet à générer (multi-sélection possible)."
)
@click.option(
    "--formats",
    type=click.Choice([f.value for f in OutputFormat], case_sensitive=False),
    multiple=True,
    help="Formats de sortie souhaités (multi-sélection possible)."
)
@click.option(
    "--versioning",
    type=click.Choice([v.value for v in VersioningSystem], case_sensitive=False),
    default=VersioningSystem.NONE.value,
    show_default=True,
    help="Système de versionnage à configurer."
)
@click.option(
    "--ci",
    type=click.Choice([c.value for c in CIOption], case_sensitive=False),
    multiple=True,
    help="Ajoute des workflows CI/CD (multi-sélection possible)."
)
@click.option(
    "--docker/--no-docker",
    default=False,
    show_default=True,
    help="Inclure un Dockerfile pour environnement reproductible."
)
@click.option(
    "--interactive",
    is_flag=True,
    help="Active le mode interactif (pose des questions à l'utilisateur)."
)
def init(
    project_name: str,
    type: str,
    formats: Optional[List[str]] = None,
    versioning: str = VersioningSystem.NONE.value,
    ci: Optional[List[str]] = None,
    docker: bool = False,
    interactive: bool = False,
):
    """
    Initialise une nouvelle structure de projet personnalisée avec support Python, Jupyter,
    Quarto Bookdown, Web App, CI/CD, Docker, et plus encore.
    """
    config = None

    if interactive:
        config = get_project_config(project_name)
    else:
        # Convert string values to enum types
        project_type = ProjectType(type)
        output_formats = [OutputFormat(f) for f in formats] if formats else None
        versioning_system = VersioningSystem(versioning)
        ci_options = [CIOption(c) for c in ci] if ci else None

        # Create configuration
        config = ProjectConfig(
            project_name=project_name,
            project_type=project_type,
            formats=output_formats,
            versioning=versioning_system,
            ci_options=ci_options,
            docker=docker,
            interactive=interactive,
        )

    console.print(f"[bold green]Configuration du projet :[/bold green]")
    console.print(f"Nom du projet: [bold]{config.project_name}[/bold]")
    console.print(f"Type de projet: [bold]{config.project_type.value}[/bold]")
    if config.formats:
        console.print(f"Formats de sortie: [bold]{', '.join(f.value for f in config.formats)}[/bold]")
    console.print(f"Système de versionnage: [bold]{config.versioning.value}[/bold]")
    if config.ci_options:
        console.print(f"Options CI/CD: [bold]{', '.join(c.value for c in config.ci_options)}[/bold]")
    console.print(f"Docker: [bold]{'Oui' if config.docker else 'Non'}[/bold]")
    console.print(f"Mode interactif: [bold]{'Oui' if config.interactive else 'Non'}[/bold]")

    # TODO: Implement project generation
    console.print("[bold yellow]Génération du projet non implémentée.[/bold yellow]")


def main():
    """Entry point for the CLI."""
    try:
        cli()
    except Exception as e:
        console.print(f"[bold red]Erreur:[/bold red] {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main() 