"""
Interactive mode for pyscaf.
"""
import questionary
from questionary import Choice
from rich.console import Console
import subprocess

from pyscaf.models import (
    CIOption,
    OutputFormat,
    ProjectConfig,
    ProjectType,
    
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
    console.print("[bold blue]Interactive project configuration[/bold blue]")
    console.print(f"Project name: [bold]{project_name}[/bold]")
    
    # Project type
    project_type_choices = [
        Choice(title=f"{pt.value} - {_get_project_type_description(pt)}", value=pt)
        for pt in ProjectType
    ]
    
    project_type = questionary.checkbox(
        "Project type?",
        choices=project_type_choices,
    ).ask()
    
    # Get git author info
    try:
        git_name = subprocess.check_output(['git', 'config', 'user.name']).decode().strip()
        git_email = subprocess.check_output(['git', 'config', 'user.email']).decode().strip()
        default_author = f"{git_name} <{git_email}>"
    except subprocess.CalledProcessError:
        default_author = ""
    
    author = questionary.text(
        "Project author?",
        default=default_author,
    ).ask()
    
    # Output formats
    format_choices = [
        Choice(title=f"{fmt.value} - {_get_format_description(fmt)}", value=fmt)
        for fmt in OutputFormat
    ]
    
    
    formats = questionary.checkbox(
        "Desired output formats?",
        choices=format_choices,
    ).ask() if ProjectType.NOTEBOOK in project_type or ProjectType.BOOK in project_type else None
    
    
    # Git
    use_git = questionary.confirm(
        "Initialize Git repository?",
        default=False,
    ).ask()
    
    # # Versioning system
    # versioning_choices = [
    #     Choice(title=f"{vs.value} - {_get_versioning_description(vs)}", value=vs)
    #     for vs in VersioningSystem
    # ]
    
    # versioning = questionary.select(
    #     "Versioning system?",
    #     choices=versioning_choices,
    #     default=VersioningSystem.NONE,
    # ).ask()
    
    # CI options
    # ci_choices = [
    #     Choice(title=f"{ci.value} - {_get_ci_description(ci)}", value=ci)
    #     for ci in CIOption
    # ]
    
    # ci_options = questionary.checkbox(
    #     "CI/CD options?",
    #     choices=ci_choices,
    # ).ask() if versioning != VersioningSystem.NONE else None
    
    # Docker
    docker = questionary.confirm(
        "Include a Dockerfile?",
        default=False,
    ).ask()
    
    # No install option
    no_install = questionary.confirm(
        "Skip installation step ?",
        default=False,
    ).ask()
    
    return ProjectConfig(
        project_name=project_name,
        project_type=project_type,
        author=author,
        formats=formats if formats else None,
        use_git=use_git,
        # ci_options=ci_options,
        docker=docker,
        interactive=True,
        no_install=no_install,
    )


def _get_project_type_description(project_type: ProjectType) -> str:
    """Get description for project type."""
    descriptions = {
        ProjectType.PACKAGE: "Installable Python package",
        ProjectType.NOTEBOOK: "Jupyter notebooks for data analysis",
        ProjectType.BOOK: "Quarto book/report for documentation",
        ProjectType.WEBAPP: "Web application for user interface",
    }
    return descriptions.get(project_type, "")


def _get_format_description(output_format: OutputFormat) -> str:
    """Get description for output format."""
    descriptions = {
        OutputFormat.HTML: "Web documentation",
        OutputFormat.PDF: "PDF document",
        OutputFormat.IPYNB: "Jupyter notebooks",
    }
    return descriptions.get(output_format, "")


# def _get_versioning_description(versioning: VersioningSystem) -> str:
#     """Get description for versioning system."""
#     descriptions = {
#         VersioningSystem.GITHUB: "Use GitHub",
#         VersioningSystem.GITLAB: "Use GitLab",
#         VersioningSystem.NONE: "No versioning configured",
#     }
    # return descriptions.get(versioning, "")


def _get_ci_description(ci_option: CIOption) -> str:
    """Get description for CI option."""
    descriptions = {
        CIOption.EXECUTE: "Run tests and notebooks",
        CIOption.BUILD: "Build package and documentation",
        CIOption.PUBLISH: "Publish package and documentation",
    }
    return descriptions.get(ci_option, "") 