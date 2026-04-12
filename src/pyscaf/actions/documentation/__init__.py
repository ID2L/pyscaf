"""Documentation scaffolding actions."""

import logging
from pathlib import Path

from pyscaf_core import Action, ChoiceOption, CLIOption

logger = logging.getLogger(__name__)

DOC_CHOICES = [
    ChoiceOption(key="none", display="None (no documentation)", value=None),
    ChoiceOption(key="pdoc", display="pdoc (simple, auto-generated API docs)", value="pdoc"),
]


class DocumentationAction(Action):
    """Action to add documentation scaffolding to the project."""

    depends = {"core"}
    run_preferably_after = "core"
    cli_options = [
        CLIOption(
            name="--documentation",
            type="choice",
            help="Choose a documentation system for your project",
            prompt="Which documentation system do you want to use?",
            choices=DOC_CHOICES,
            default=0,
        ),
    ]

    def __init__(self, project_path):
        super().__init__(project_path)

    def skeleton(self, context: dict) -> dict[Path, str | None]:
        doc_key = context.get("documentation", "none")

        doc_choice = None
        for choice in DOC_CHOICES:
            if choice.key == doc_key:
                doc_choice = choice.value
                break

        skeleton = {}
        if doc_choice == "pdoc":
            doc_readme_path = Path(__file__).parent / "README.md"
            doc_readme = doc_readme_path.read_text() if doc_readme_path.exists() else ""

            skeleton[Path("README.md")] = doc_readme

            scripts_dir = Path(__file__).parent / "scripts"
            if scripts_dir.exists():
                skeleton[Path("src/pyscaf/__init__.py")] = ""
                skeleton[Path("src/pyscaf/documentation/__init__.py")] = ""
                skeleton[Path("src/pyscaf/documentation/scripts/__init__.py")] = ""

                for script_file in scripts_dir.glob("*.py"):
                    script_content = script_file.read_text()
                    skeleton[Path(f"src/pyscaf/documentation/scripts/{script_file.name}")] = script_content
        return skeleton

    def init(self, context):
        doc_key = context.get("documentation", "none")
        if doc_key == "none":
            return

        super().init(context)
