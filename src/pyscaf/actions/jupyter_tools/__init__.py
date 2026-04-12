"""Jupyter tools initialization actions."""

import logging
import os
from pathlib import Path

import tomli
from pyscaf_core import Action, CLIOption

logger = logging.getLogger(__name__)


class JupyterToolsAction(Action):
    """Action to provide Jupyter notebook manipulation tools."""

    depends = {"jupyter"}
    run_preferably_after = "jupyter"
    cli_options = [
        CLIOption(
            name="--jupyter_tools",
            type="bool",
            help="Add Jupyter notebook manipulation tools",
            prompt="Do you want to add Jupyter notebook manipulation tools ?",
            default=False,
        ),
    ]

    def __init__(self, project_path):
        super().__init__(project_path)

    def activate(self, context: dict) -> bool:
        return (
            context.get("jupyter", True) and context.get("jupyter_tools") is None or context.get("jupyter_tools", True)
        )

    def skeleton(self, context: dict) -> dict[Path, str | None]:
        config_path = Path(__file__).parent / "config.toml"
        readme_path = Path(__file__).parent / "README.md"
        readme_content = readme_path.read_text() if readme_path.exists() else ""
        config_content = config_path.read_text() if config_path.exists() else ""

        config_dirs = []
        if config_path.exists():
            try:
                config_data = tomli.loads(config_content)
                if (
                    "tool" in config_data
                    and "pyscaf" in config_data["tool"]
                    and "jupyter_tools" in config_data["tool"]["pyscaf"]
                ):
                    jupyter_tools_config = config_data["tool"]["pyscaf"]["jupyter_tools"]
                    for key, value in jupyter_tools_config.items():
                        if isinstance(value, str) and ("dir" in key or "directory" in key):
                            config_dirs.append(Path(value))
            except Exception as e:
                logger.warning("Could not parse config.toml: %s", e)

        scripts_dir = Path(__file__).parent / "scripts"

        skeleton = {
            Path("src/pyscaf/jupyter_tools"): None,
            Path("README.md"): readme_content,
        }

        for dir_path in config_dirs:
            skeleton[dir_path] = None

        if scripts_dir.exists():
            skeleton[Path("src/pyscaf/__init__.py")] = ""
            skeleton[Path("src/pyscaf/jupyter_tools/__init__.py")] = ""
            skeleton[Path("src/pyscaf/jupyter_tools/scripts/__init__.py")] = ""

            for script_file in scripts_dir.glob("*.py"):
                script_content = script_file.read_text()
                skeleton[Path(f"src/pyscaf/jupyter_tools/scripts/{script_file.name}")] = script_content

        return skeleton

    def install(self, context: dict) -> None:
        logger.info("Setting up Jupyter tools...")

        try:
            os.chdir(self.project_path)

            tools_dir = Path("tools")
            if tools_dir.exists():
                for script_file in tools_dir.glob("*.py"):
                    try:
                        script_file.chmod(0o755)
                        logger.info("Made %s executable", script_file.name)
                    except OSError:
                        pass

            logger.info("Jupyter tools setup complete!")

        except Exception as e:
            logger.warning("Error setting up Jupyter tools: %s", e)
