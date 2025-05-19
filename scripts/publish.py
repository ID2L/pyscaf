"""
Script to handle package publication with environment variables.
"""
import os
import sys
import subprocess
from enum import Enum
from pathlib import Path
from typing import NoReturn

import click
from dotenv import load_dotenv


class PublishTarget(str, Enum):
    """Enum for publish targets."""
    GITHUB = "github"
    PYPI = "pypi"
    BOTH = "both"


def load_env() -> None:
    """Load environment variables from .env file."""
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
    else:
        print("Warning: No .env file found. Make sure your environment variables are set.")


def check_required_env(target: PublishTarget) -> None:
    """Check if required environment variables are set based on target.
    
    Args:
        target: The target platform(s) to publish to
    """
    required_vars = []
    if target in [PublishTarget.GITHUB, PublishTarget.BOTH]:
        required_vars.append("GH_TOKEN")
    if target in [PublishTarget.PYPI, PublishTarget.BOTH]:
        required_vars.append("PYPI_TOKEN")
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing_vars)}"
        )


@click.command()
@click.option(
    "--target",
    type=click.Choice([t.value for t in PublishTarget], case_sensitive=False),
    default=PublishTarget.BOTH.value,
    help="Target platform to publish to (github, pypi, or both)",
)
@click.option(
    "--prerelease/--no-prerelease",
    default=True,
    help="Whether to publish as a prerelease version",
)
def publish(target: str, prerelease: bool) -> NoReturn:
    """Run semantic-release publish command with environment variables.
    
    Args:
        target: The target platform(s) to publish to
        prerelease: Whether to publish as a prerelease version
    """
    target_enum = PublishTarget(target)
    load_env()
    check_required_env(target_enum)
    
    try:
        # Configure semantic-release based on target
        if target_enum == PublishTarget.GITHUB:
            os.environ["SEMANTIC_RELEASE_PUBLISH"] = "github"
        elif target_enum == PublishTarget.PYPI:
            os.environ["SEMANTIC_RELEASE_PUBLISH"] = "pypi"
        # For BOTH, we use the default configuration
        
        # Configure prerelease
        if prerelease:
            os.environ["SEMANTIC_RELEASE_PRERELEASE"] = "true"
            os.environ["SEMANTIC_RELEASE_PRERELEASE_TOKEN"] = "alpha"
        
        result = subprocess.run(["semantic-release", "publish"], check=True)
        sys.exit(result.returncode)
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)


if __name__ == "__main__":
    publish()
