from .dependency_loader import load_and_complete_dependencies
from .tree_walker import DependencyTreeWalker
import os

if __name__ == '__main__':
    # Load and complete dependencies from YAML
    yaml_path = os.path.join(os.path.dirname(__file__), 'dependencies.yaml')
    dependencies = load_and_complete_dependencies(yaml_path)
    # Example usage: build and print the tree from a root id
    root_id = 'test'  # Change as needed
    tree_walker = DependencyTreeWalker(dependencies, root_id)
    tree_walker.print_tree() 