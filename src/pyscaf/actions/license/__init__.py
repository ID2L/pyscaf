from pathlib import Path
from typing import Dict, Optional

from pyscaf.actions import Action, CLIOption

LICENSES = {
    "MIT": "template_MIT.txt",
    "Apache-2.0": "template_Apache-2.0.txt",
    "GPL-3.0": "template_GPL-3.0.txt",
    "BSD-3-Clause": "template_BSD-3-Clause.txt",
    "Mozilla": "template_MPL-2.0.txt",
    "Unlicense": "template_Unlicense.txt",
}


class LicenseAction(Action):
    """Action to add a LICENSE file to the project."""

    depends = {"core"}
    run_preferably_after = "core"
    cli_options = [
        CLIOption(
            name="--license",
            type="choice",
            help="Choose a license for your project",
            prompt="Which license do you want to use?",
            choices=list(LICENSES.keys()),
            default="MIT",
        ),
    ]

    def __init__(self, project_path):
        super().__init__(project_path)

    def skeleton(self, context: dict) -> Dict[Path, Optional[str]]:
        """
        Define the filesystem skeleton for License initialization.
        Returns: Dictionary mapping paths to content
        """
        import datetime

        license_name = context.get("license", "MIT")
        template_file = LICENSES.get(license_name, LICENSES["MIT"])
        template_path = Path(__file__).parent / template_file
        license_content = (
            template_path.read_text()
            if template_path.exists()
            else f"{license_name} License"
        )
        year = str(datetime.datetime.now().year)
        author = context.get("author", "")
        license_content = license_content.replace("{year}", year).replace(
            "{author}", author
        )
        return {Path("LICENSE"): license_content}

    def init(self, context: dict) -> None:
        pass

    def install(self, context: dict) -> None:
        pass
