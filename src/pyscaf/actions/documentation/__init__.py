from pathlib import Path

from pyscaf.actions import Action, ChoiceOption, CLIOption

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
            default=0,  # Index of the default choice
        ),
    ]

    def __init__(self, project_path):
        super().__init__(project_path)

    def skeleton(self, context: dict) -> dict[Path, str | None]:
        doc_key = context.get("documentation", "none")  # Get the key (e.g., "none", "pdoc")
        print(f"Documentation key: {doc_key}")

        # Convert key to value using DOC_CHOICES directly
        doc_choice = None
        for choice in DOC_CHOICES:
            if choice.key == doc_key:
                doc_choice = choice.value
                break
        print(f"Documentation choice value: {doc_choice}")

        skeleton = {}
        if doc_choice == "pdoc":
            # Read documentation README
            doc_readme_path = Path(__file__).parent / "README.md"
            doc_readme = doc_readme_path.read_text() if doc_readme_path.exists() else ""

            skeleton[Path("README.md")] = doc_readme

            # Copy scripts from the source
            scripts_dir = Path(__file__).parent / "scripts"
            if scripts_dir.exists():
                # Add __init__.py for pyscaf directory
                skeleton[Path("pyscaf/__init__.py")] = ""
                skeleton[Path("pyscaf/documentation/__init__.py")] = ""
                skeleton[Path("pyscaf/documentation/scripts/__init__.py")] = ""

                for script_file in scripts_dir.glob("*.py"):
                    script_content = script_file.read_text()
                    skeleton[Path(f"pyscaf/documentation/scripts/{script_file.name}")] = script_content
        # If doc_choice is None, do not add anything
        return skeleton

    def init(self, context):
        doc_key = context.get("documentation", "none")  # Get the key (e.g., "none", "pdoc")
        if doc_key == "none":
            return

        super().init(context)

        # Post-process pyproject.toml to replace placeholders
        project_name = context.get("project_name", "myproject")
        package_name = context.get("package_name", project_name.replace("-", "_"))

        pyproject_path = self.project_path / "pyproject.toml"
        if pyproject_path.exists():
            content = pyproject_path.read_text()
            # Replace both {package_name} and {curated_project_name} for compatibility
            placeholders = ["{package_name}", "{curated_project_name}"]
            new_content = content
            for placeholder in placeholders:
                if placeholder in new_content:
                    new_content = new_content.replace(placeholder, package_name)
            
            if new_content != content:
                pyproject_path.write_text(new_content)
                print(f"[INFO] Replaced placeholders in {pyproject_path}")
