from .dependency_loader import load_and_complete_dependencies
from .tree_walker import DependencyTreeWalker
from .topologic_tree import best_execution_order
import os

if __name__ == '__main__':
    # Load and complete dependencies from YAML
    yaml_path = os.path.join(os.path.dirname(__file__), 'dependencies.yaml')
    dependencies = load_and_complete_dependencies(yaml_path)
    # Example usage: build and print the tree from a root id
    nodes = []
    for root_id in ['test', 'jupyter', 'versionning']:
        tree_walker = DependencyTreeWalker(dependencies, root_id)
        tree_walker.print_tree()
        node = {
            "id": root_id,
            "fullfilled": list(tree_walker.fullfilled_depends),
            "external": list(tree_walker.external_depends)
        }
        nodes.append(node)
    print("Best execution order:", best_execution_order(nodes)) 