from pathlib import Path
from typing import Dict, Optional

from pyscaf.actions import Action, CLIOption

DOC_TYPES = {
    "None (no documentation)": None,
    "pdoc (simple, auto-generated API docs)": "pdoc",
}


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
            choices=list(DOC_TYPES.keys()),
            default=list(DOC_TYPES.keys())[0],
        ),
    ]

    def __init__(self, project_path):
        super().__init__(project_path)

    def skeleton(self, context: dict) -> Dict[Path, Optional[str]]:
        doc_choice = context.get("documentation", list(DOC_TYPES.keys())[0])
        doc_type = DOC_TYPES.get(doc_choice, "pdoc")
        skeleton = {}
        if doc_type == "pdoc":
            skeleton[Path("docs/README.md")] = (
                "# API Documentation\n\nThis documentation is auto-generated using [pdoc](https://pdoc.dev/).\n"
            )
            skeleton[Path("docs/.gitkeep")] = ""  # To keep the docs folder in git

            # Copy scripts from the source
            scripts_dir = Path(__file__).parent / "scripts"
            if scripts_dir.exists():
                # Add __init__.py for pyscaf directory
                skeleton[Path("pyscaf/__init__.py")] = ""
                skeleton[Path("pyscaf/documentation/__init__.py")] = ""
                skeleton[Path("pyscaf/documentation/scripts/__init__.py")] = ""

                for script_file in scripts_dir.glob("*.py"):
                    script_content = script_file.read_text()
                    skeleton[
                        Path(f"pyscaf/documentation/scripts/{script_file.name}")
                    ] = script_content
        # If doc_type is None, do not add anything
        return skeleton

    def install(self, context: dict) -> None:
        pass

    def activate(self, context: dict) -> bool:
        doc_choice = context.get("documentation", list(DOC_TYPES.keys())[0])
        doc_type = DOC_TYPES.get(doc_choice, "pdoc")
        return doc_type is not None
