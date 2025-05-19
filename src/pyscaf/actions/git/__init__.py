"""
Git initialization actions.
"""
import os
import subprocess
from pathlib import Path
from typing import Dict, Optional

import questionary
from rich.console import Console

from pyscaf.actions import Action
from pyscaf.models import ProjectConfig, VersioningSystem

console = Console()


class GitAction(Action):
    """Action to initialize a Git repository in a project."""
    
    def skeleton(self) -> Dict[Path, Optional[str]]:
        """
        Define the filesystem skeleton for Git initialization.
        
        Returns:
            Dictionary mapping paths to content
        """
        # Read Git documentation
        git_doc_path = Path(__file__).parent / "README.md"
        git_doc = git_doc_path.read_text() if git_doc_path.exists() else ""
        
        # Python & Poetry .gitignore content
        gitignore_content = """### Python ###
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# celery beat schedule file
celerybeat-schedule

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

### Poetry ###
# Poetry local configuration file - https://python-poetry.org/docs/configuration/#local-configuration
poetry.toml

# Poetry lock file for demo projects
poetry.lock

# Local history for Visual Studio Code
.history/

# Built Visual Studio Code extensions
*.vsix

# IDE settings
.idea/
.vscode/
*.swp
*.swo
"""
        
        # Return skeleton dictionary
        return {
            Path(".gitignore"): gitignore_content,
            Path("README.md"): git_doc,  # Add Git documentation to README.md
        }
    
    def init(self) -> None:
        """
        Initialize Git repository after skeleton creation.
        
        This will initialize a Git repository and optionally add a remote.
        """
        console.print("[bold blue]Initializing Git repository...[/bold blue]")
        
        try:
            # Change to project directory
            os.chdir(self.project_path)
            
            # Initialize Git repository
            console.print("[bold cyan]Running git init...[/bold cyan]")
            
            # Use subprocess.call to run git commands
            result = subprocess.call(
                ["git", "init"],
                stdin=None,
                stdout=None,
                stderr=None,
            )
            
            if result == 0:
                console.print("[bold green]Git repository initialized successfully![/bold green]")
                
                # Configure remote repository if using GitHub or GitLab
                self._configure_remote()
            else:
                console.print(f"[bold yellow]Git init exited with code {result}[/bold yellow]")
            
        except FileNotFoundError:
            console.print("[bold yellow]Git not found. Please install it first.[/bold yellow]")
    
    def _configure_remote(self) -> None:
        """Configure remote repository."""
        # Ask for remote URL
        remote_url = questionary.text(
            f"Enter remote URL for {self.config.versioning.value} repository (leave empty to configure later):",
            default="",
        ).ask()
        
        if remote_url:
            # Add remote
            result = subprocess.call(
                ["git", "remote", "add", "origin", remote_url],
                stdin=None,
                stdout=None,
                stderr=None,
            )
            
            if result == 0:
                console.print(f"[bold green]Remote repository configured: {remote_url}[/bold green]")
                
                # Ask if user wants to push to remote
                should_push = questionary.confirm(
                    "Push to remote repository now?",
                    default=False,
                ).ask()
                
                if should_push:
                    # Push to remote
                    subprocess.call(
                        ["git", "push", "-u", "origin", "main"],
                        stdin=None,
                        stdout=None,
                        stderr=None,
                    )
            else:
                console.print(f"[bold yellow]Failed to add remote (exit code {result})[/bold yellow]")
        else:
            console.print("[bold blue]No remote URL provided. You can add it later with:[/bold blue]")
            console.print("  git remote add origin <your-repository-url>")
    
    def install(self) -> None:
        """
        No additional installation steps needed for Git.
        """
        # Add files to repository
        subprocess.call(
            ["git", "add", "."],
            stdin=None,
            stdout=None,
            stderr=None,
        )
        
        # Initial commit
        subprocess.call(
            ["git", "commit", "-m", "feat: Initial commit"],
            stdin=None,
            stdout=None,
            stderr=None,
        )
        