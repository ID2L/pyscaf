"""
Interactive mode for pyscaf.
"""
import questionary
from questionary import Choice
from rich.console import Console

from pyscaf.models import (
    CIOption,
    OutputFormat,
    ProjectConfig,
    ProjectType,
    VersioningSystem,
)

console = Console()


def get_project_config(project_name: str) -> ProjectConfig:
    """
    Interactive mode to configure a new project.
    
    Args:
        project_name: Name of the project
        
    Returns:
        ProjectConfig: Configuration for the project
    """
    console.print("[bold blue]Configuration interactive du projet[/bold blue]")
    console.print(f"Nom du projet: [bold]{project_name}[/bold]")
    
    # Project type
    project_type_choices = [
        Choice(title=f"{pt.value} - {_get_project_type_description(pt)}", value=pt)
        for pt in ProjectType
    ]
    
    project_type = questionary.select(
        "Type de projet ?",
        choices=project_type_choices,
    ).ask()
    
    # Output formats
    format_choices = [
        Choice(title=f"{fmt.value} - {_get_format_description(fmt)}", value=fmt)
        for fmt in OutputFormat
    ]
    
    formats = questionary.checkbox(
        "Formats de sortie souhaités ?",
        choices=format_choices,
    ).ask()
    
    # Versioning system
    versioning_choices = [
        Choice(title=f"{vs.value} - {_get_versioning_description(vs)}", value=vs)
        for vs in VersioningSystem
    ]
    
    versioning = questionary.select(
        "Système de versionnage ?",
        choices=versioning_choices,
        default=VersioningSystem.NONE,
    ).ask()
    
    # CI options
    ci_choices = [
        Choice(title=f"{ci.value} - {_get_ci_description(ci)}", value=ci)
        for ci in CIOption
    ]
    
    ci_options = questionary.checkbox(
        "Options CI/CD ?",
        choices=ci_choices,
    ).ask() if versioning != VersioningSystem.NONE else None
    
    # Docker
    docker = questionary.confirm(
        "Inclure un Dockerfile ?",
        default=False,
    ).ask()
    
    return ProjectConfig(
        project_name=project_name,
        project_type=project_type,
        formats=formats if formats else None,
        versioning=versioning,
        ci_options=ci_options,
        docker=docker,
        interactive=True,
    )


def _get_project_type_description(project_type: ProjectType) -> str:
    """Get description for project type."""
    descriptions = {
        ProjectType.PACKAGE: "Package Python installable",
        ProjectType.NOTEBOOK: "Notebooks Jupyter pour analyse de données",
        ProjectType.BOOK: "Livre/rapport Quarto pour documentation",
        ProjectType.WEBAPP: "Application web pour interface utilisateur",
    }
    return descriptions.get(project_type, "")


def _get_format_description(output_format: OutputFormat) -> str:
    """Get description for output format."""
    descriptions = {
        OutputFormat.HTML: "Documentation web",
        OutputFormat.PDF: "Document PDF",
        OutputFormat.IPYNB: "Notebooks Jupyter",
    }
    return descriptions.get(output_format, "")


def _get_versioning_description(versioning: VersioningSystem) -> str:
    """Get description for versioning system."""
    descriptions = {
        VersioningSystem.GITHUB: "Utiliser GitHub",
        VersioningSystem.GITLAB: "Utiliser GitLab",
        VersioningSystem.NONE: "Pas de versionnage configuré",
    }
    return descriptions.get(versioning, "")


def _get_ci_description(ci_option: CIOption) -> str:
    """Get description for CI option."""
    descriptions = {
        CIOption.EXECUTE: "Exécuter tests et notebooks",
        CIOption.BUILD: "Construire package et documentation",
        CIOption.PUBLISH: "Publier package et documentation",
    }
    return descriptions.get(ci_option, "") 