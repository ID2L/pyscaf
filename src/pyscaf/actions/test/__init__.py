"""Test initialization actions using pytest."""

import logging
import os
import subprocess
from pathlib import Path

from pyscaf_core import Action, CLIOption

logger = logging.getLogger(__name__)


class TestAction(Action):
    """Action to initialize a project with pytest testing framework."""

    depends = {"core", "git"}
    run_preferably_after = "git"
    cli_options = [
        CLIOption(
            name="--testing",
            type="bool",
            help="Enable testing with pytest",
            prompt="Do you want to set up testing with pytest?",
            default=False,
        ),
    ]

    def __init__(self, project_path):
        super().__init__(project_path)

    def activate(self, context: dict) -> bool:
        return context.get("testing") is None or context.get("testing", True)

    def skeleton(self, context: dict) -> dict[Path, str | None]:
        pytest_doc_path = Path(__file__).parent / "README.md"
        pytest_doc = pytest_doc_path.read_text() if pytest_doc_path.exists() else ""

        test_example_path = Path(__file__).parent / "template_test_example.py"
        test_example_template = test_example_path.read_text() if test_example_path.exists() else ""

        project_name = context.get("project_name", "myproject")
        curated_project_name = project_name.replace("-", "_")

        test_example = test_example_template.format(
            project_name=project_name, curated_project_name=curated_project_name
        )

        skeleton = {
            Path("tests"): None,
            Path("tests/__init__.py"): "",
            Path(f"tests/test_{curated_project_name}.py"): test_example,
            Path("tests/README.md"): pytest_doc,
        }
        if context.get("versionning"):
            gitignore_path = Path(__file__).parent / "template.gitignore"
            gitignore_content = gitignore_path.read_text() if gitignore_path.exists() else ""
            skeleton[Path(".gitignore")] = gitignore_content
        return skeleton

    def install(self, context: dict) -> None:
        logger.info("Installing test dependencies...")

        try:
            os.chdir(self.project_path)

            env = os.environ.copy()
            env.pop("VIRTUAL_ENV", None)

            result = subprocess.call(
                ["uv", "run", "pytest", "--version"],
                env=env,
                stdin=None,
                stdout=None,
                stderr=None,
            )

            if result == 0:
                logger.info("Pytest setup validated successfully!")

                test_result = subprocess.call(
                    ["uv", "run", "pytest", "tests/", "-v"],
                    env=env,
                    stdin=None,
                    stdout=None,
                    stderr=None,
                )

                if test_result == 0:
                    logger.info("All tests passed!")
                else:
                    logger.warning("Some tests failed (exit code %s)", test_result)
            else:
                logger.warning("Pytest validation failed (exit code %s)", result)

        except FileNotFoundError:
            logger.warning("uv not found. Please install it first.")
            logger.info("https://docs.astral.sh/uv/getting-started/installation")
