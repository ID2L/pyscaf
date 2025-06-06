import logging
import os
import sys

from pyscaf.preference_chain.new_preference_chain import (
    build_chains,
    compute_all_resolution_pathes,
    compute_path_score,
    extend_nodes,
)

from .dependency_loader import load_and_complete_dependencies
from .topologic_tree import best_execution_order
from .tree_walker import DependencyTreeWalker

# Utility to get direct dependants of a node
# Returns the list of Node that directly depend on parent_id


def get_direct_dependants(dependencies, parent_id):
    """Return the list of Node that directly depend on parent_id."""
    return [dep for dep in dependencies if dep.depends and parent_id in dep.depends]


# Utility to build a node for best_execution_order
# Uses DependencyTreeWalker to compute the fullfilled and external dependencies for a given node


def build_node(dep, dependencies):
    walker = DependencyTreeWalker(dependencies, dep.id)
    return {
        "id": dep.id,
        "fullfilled": list(walker.fullfilled_depends),
        "external": list(walker.external_depends),
    }


# Recursive function to build the optimal order
# For a given current_id, finds all direct dependants, orders them optimally,
# and recursively applies the same logic to each dependant.
# The result is a flattened list starting with current_id, followed by the optimal order of all subtrees.


def recursive_best_order(dependencies, current_id):
    direct_dependants = get_direct_dependants(dependencies, current_id)
    print(f"Current id: {current_id}")
    print(f"Direct dependants: {direct_dependants}")
    if not direct_dependants:
        print(f"No direct dependants for {current_id}, added to the pile")
        return [current_id]
    nodes = [build_node(dep, dependencies) for dep in direct_dependants]
    local_order = best_execution_order(nodes)
    result = [current_id]
    for node_id in local_order:
        result.extend(recursive_best_order(dependencies, node_id))
    return result


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    if "-v" in sys.argv:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(levelname)s %(name)s::%(funcName)s: \n    %(message)s",
        )
        logger.debug("Mode debug activé")
    else:
        logging.basicConfig(
            level=logging.WARNING, format="\n    %(levelname)s: %(message)s"
        )

    # Load and complete dependencies from YAML
    yaml_path = os.path.join(os.path.dirname(__file__), "dependencies.yaml")
    dependencies = load_and_complete_dependencies(yaml_path)
    tree = DependencyTreeWalker(dependencies, "root")
    extended_dependencies = extend_nodes(dependencies)
    # for dep in extended_dependencies:
    #     print(dep)
    #     print("\n")
    clusters = build_chains(extended_dependencies)

    # for cluster in clusters:
    #     logger.debug(cluster)
    #     print("\n")
    # logger.debug(tree.print_tree())
    all_resolution_pathes = list(compute_all_resolution_pathes(clusters))
    logger.debug(f"Found {len(all_resolution_pathes)} resolution pathes")
    all_resolution_pathes.sort(key=lambda path: -compute_path_score(list(path)))
    for path in all_resolution_pathes:
        logger.debug(f"Score : {compute_path_score(path)}")
        for chain in list(path):
            logger.debug(f"Chain: {chain.ids}")
