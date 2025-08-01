"""
Action classes for project scaffolding.
"""

import importlib
import logging
import os
import pkgutil
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Union

from pydantic import BaseModel

from pyscaf.tools.format_toml import format_toml
from pyscaf.tools.toml_merge import merge_toml_files

logger = logging.getLogger(__name__)


class ChoiceOption(BaseModel):
    """Represents a choice option with different display formats for CLI and interactive modes.

    This class allows you to define choices with:
    - key: Short identifier for CLI usage (e.g., "mit", "pdoc")
    - display: Verbose description for interactive mode (e.g., "MIT License (permissive)")
    - value: The actual value stored in context (e.g., "template_MIT.txt")

    Example:
        choices = [
            ChoiceOption(
                key="mit",
                display="MIT License (permissive, suitable for most projects)",
                value="template_MIT.txt"
            ),
            ChoiceOption(
                key="apache",
                display="Apache-2.0 License (permissive, protects against patent claims)",
                value="template_Apache-2.0.txt"
            ),
        ]

        option = CLIOption(
            name="--license",
            type="choice",
            choices=choices,
            default=0  # Index of the default choice
        )
    """

    key: str  # Short key for CLI usage
    display: str  # Verbose display for interactive mode
    value: Any  # The actual value to be stored in context


class CLIOption(BaseModel):
    name: str  # e.g. '--author'
    type: str = "str"  # 'str', 'bool', 'int', 'choice', etc.
    help: Optional[str] = None
    default: Any = None  # For choice type, this should be an index (int)
    prompt: Optional[str] = None
    choices: Optional[List[ChoiceOption]] = (
        None  # For choice type - can be List[str] or List[ChoiceOption]
    )
    is_flag: Optional[bool] = None  # For bool
    multiple: Optional[bool] = None  # For multi-choice
    required: Optional[bool] = None

    def get_choice_keys(self) -> List[str]:
        """Get the list of choice keys for CLI usage."""
        if self.choices and isinstance(self.choices[0], ChoiceOption):
            return [choice.key for choice in self.choices]
        return []

    def get_choice_displays(self) -> List[str]:
        """Get the list of choice displays for interactive mode."""
        if self.choices and isinstance(self.choices[0], ChoiceOption):
            return [choice.display for choice in self.choices]
        return []

    def get_choice_values(self) -> List[Any]:
        """Get the list of choice values."""
        if self.choices and isinstance(self.choices[0], ChoiceOption):
            return [choice.value for choice in self.choices]
        return []

    def get_choice_by_key(self, key: str) -> Optional[Any]:
        """Get the value corresponding to a choice key."""

        if self.choices and isinstance(self.choices[0], ChoiceOption):
            for choice in self.choices:
                if choice.key == key:
                    return choice.value
        return None

    def get_choice_by_display(self, display: str) -> Optional[Any]:
        """Get the value corresponding to a choice display."""

        if self.choices and isinstance(self.choices[0], ChoiceOption):
            for choice in self.choices:
                if choice.display == display:
                    return choice.value
        return None

    def get_default_display(self) -> Optional[str]:
        """Get the default display."""
        if self.type == "choice" and self.choices and isinstance(self.default, int):
            if 0 <= self.default < len(self.choices):
                if isinstance(self.choices[0], ChoiceOption):
                    return self.choices[self.default].display
        return None

    def get_default_value(self) -> Any:
        """Get the default value, handling both index and direct value."""
        if self.type == "choice" and self.choices and isinstance(self.default, int):
            # Default is an index
            if 0 <= self.default < len(self.choices):
                if isinstance(self.choices[0], ChoiceOption):
                    return self.choices[self.default].value
                else:
                    return self.choices[self.default]
        return self.default


class Action(ABC):
    """
    Abstract base class for all project actions.
    Now supports explicit dependencies, preferences, and CLI options.

    Actions can:
    1. Generate file/directory skeleton via the skeleton() method
    2. Initialize content/behavior via the init() method
    3. Install dependencies via the install() method
    """

    # Explicit dependencies and preferences
    depends: set[str] = set()
    run_preferably_after: Optional[str] = None
    cli_options: List[CLIOption] = []

    def __init_subclass__(cls):
        # Validation: if multiple depends and no run_preferably_after, raise error
        if (
            hasattr(cls, "depends")
            and len(cls.depends) > 1
            and not getattr(cls, "run_preferably_after", None)
        ):
            raise ValueError(
                f"Action '{cls.__name__}' has multiple depends but no run_preferably_after"
            )

    def __init__(self, project_path: Union[str, Path]):
        self.project_path = Path(project_path)

    @abstractmethod
    def skeleton(self, context: dict) -> Dict[Path, Optional[str]]:
        """
        Define the filesystem skeleton for this action, using the provided context.

        Returns a dictionary mapping paths to create to their content:
        - If the value is None, a directory is created
        - If the value is a string, a file is created with that content

        Returns:
            Dictionary mapping paths to content
        """
        pass

    def init(self, context: dict) -> None:
        """
        Default implementation: merges config.toml from the concrete action's directory into pyproject.toml in the project root (if it exists).
        """
        # Find the module where the concrete action is defined
        module = importlib.import_module(self.__class__.__module__)
        module_file = module.__file__
        if not module_file:
            raise RuntimeError(f"Module {module} has no __file__ attribute")
        action_dir = Path(module_file).parent
        config_path = action_dir / "config.toml"
        pyproject_path = self.project_path / "pyproject.toml"
        if config_path.exists():
            merge_toml_files(input_path=config_path, output_path=pyproject_path)
            format_toml(pyproject_path)
            print(f"[INFO] Merged {config_path} into {pyproject_path}")

    def install(self, context: dict) -> None:
        """
        Install dependencies or run post-initialization commands, using the provided context.

        This method is called after all actions have been initialized.
        Use it to install dependencies, run commands like 'poetry install', etc.
        """
        pass

    def create_skeleton(self, context: dict) -> Set[Path]:
        """
        Create the filesystem skeleton for this action using the provided context.

        Returns:
            Set of paths created
        """
        created_paths = set()
        skeleton = self.skeleton(context)

        for path, content in skeleton.items():
            full_path = self.project_path / path

            # Create parent directories if they don't exist
            full_path.parent.mkdir(parents=True, exist_ok=True)

            if content is None:
                # Create directory
                full_path.mkdir(exist_ok=True)
            else:
                # Create file with content or append if exists
                if full_path.exists():
                    # Append content to existing file
                    print(f"Appending content to {full_path}")
                    with open(full_path, "a") as f:
                        f.write("\n" + content)
                else:
                    # Create new file with content
                    full_path.write_text(content)

            created_paths.add(full_path)

        return created_paths

    def activate(self, context: dict) -> bool:
        """
        Return True if this action's question/step should be executed given the current context.
        Override in subclasses for conditional logic.
        """
        return True


def discover_actions():
    """
    Dynamically discover all Action subclasses in the actions package (excluding base/manager/pycache).
    Returns a list of Action classes.
    """
    actions: List[type[Action]] = []
    actions_dir = os.path.dirname(__file__)
    for _, module_name, is_pkg in pkgutil.iter_modules([actions_dir]):
        if module_name in ("base", "manager", "__pycache__"):
            continue
        mod = importlib.import_module(f"pyscaf.actions.{module_name}")
        for attr in dir(mod):
            obj = getattr(mod, attr)
            if isinstance(obj, type) and issubclass(obj, Action) and obj is not Action:
                actions.append(obj)
    return actions
