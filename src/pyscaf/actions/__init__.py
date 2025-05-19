"""
Action classes for project scaffolding.
"""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional, Set, Union

from pyscaf.models import ProjectConfig


class Action(ABC):
    """
    Abstract base class for all project actions.
    
    Actions can:
    1. Generate file/directory skeleton via the skeleton() method
    2. Initialize content/behavior via the init() method
    3. Install dependencies via the install() method
    """
    
    def __init__(self, project_path: Union[str, Path], config: ProjectConfig):
        """
        Initialize the action.
        
        Args:
            project_path: Path to the project directory
            config: Project configuration
        """
        self.project_path = Path(project_path)
        self.config = config
    
    @abstractmethod
    def skeleton(self) -> Dict[Path, Optional[str]]:
        """
        Define the filesystem skeleton for this action.
        
        Returns a dictionary mapping paths to create to their content:
        - If the value is None, a directory is created
        - If the value is a string, a file is created with that content
        
        Returns:
            Dictionary mapping paths to content
        """
        pass
    
    def init(self) -> None:
        """
        Initialize the action after skeleton creation.
        
        This method is called after all skeletons have been created.
        Use it to run tools, modify files, etc.
        """
        pass
    
    def install(self) -> None:
        """
        Install dependencies or run post-initialization commands.
        
        This method is called after all actions have been initialized.
        Use it to install dependencies, run commands like 'poetry install', etc.
        """
        pass
    
    def create_skeleton(self) -> Set[Path]:
        """
        Create the filesystem skeleton for this action.
        
        Returns:
            Set of paths created
        """
        created_paths = set()
        skeleton = self.skeleton()
        
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
                    with open(full_path, 'a') as f:
                        f.write('\n' + content)
                else:
                    # Create new file with content
                    full_path.write_text(content)
                
            created_paths.add(full_path)
        
        return created_paths 