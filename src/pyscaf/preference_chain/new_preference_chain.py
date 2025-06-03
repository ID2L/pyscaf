from typing import List

from pydantic import BaseModel

satisfied = set[str]()
executed = set[str]()


class Node(BaseModel):
    id: str
    depends: List[str] = []
    after: str | None = None


def build_subtree(tree: list[Node], node: Node) -> list[Node]:
    # Start with the current node
    subtree = [node]

    # Find all nodes that have this node's id as their 'after' field
    children = [n for n in tree if n.after == node.id]

    # Recursively build subtrees for each child
    for child in children:
        # Add child's subtree to our result
        subtree.extend(build_subtree(tree, child))

    return subtree


def find_external_dependencies(tree: list[Node], satisfied: set[str]) -> set[str]:
    # Find all unsatisfied dependency names across all nodes
    external_dependencies: set[str] = set()

    # Get all node IDs in the tree
    tree_node_ids = {node.id for node in tree}

    for node in tree:
        # Check each dependency of the node
        for dependency in node.depends:
            # If dependency not in tree nodes and not satisfied, add it to external dependencies
            if dependency not in tree_node_ids and dependency not in satisfied:
                external_dependencies.add(dependency)

    return external_dependencies
