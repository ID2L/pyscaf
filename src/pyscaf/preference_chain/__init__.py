import logging
from typing import List

from pyscaf.preference_chain.chain import (
    build_chains,
    compute_all_resolution_pathes,
    compute_path_score,
    extend_nodes,
)
from pyscaf.preference_chain.model import Node

from .dependency_loader import load_and_complete_dependencies
from .model import Node
from .tree_walker import DependencyTreeWalker

logger = logging.getLogger(__name__)


class CircularDependencyError(Exception):
    """Raised when circular dependencies or unsatisfiable constraints are detected."""

    pass


def best_execution_order(nodes: List[dict]) -> List[str]:
    """
    Determine the best execution order using the preference chain logic.

    Args:
        nodes: List of dictionaries with 'id', 'fullfilled', and 'external' keys

    Returns:
        List of node IDs in optimal execution order

    Raises:
        CircularDependencyError: If no valid resolution path can be found
    """
    # Convert the input format to Node objects
    node_objects = []
    for node in nodes:
        node_id = node["id"]
        external_deps = node.get("external", [])
        # In the new system, we use 'depends' for external dependencies
        # and we need to determine 'after' preference if there's only one dependency
        after = external_deps[0] if len(external_deps) == 1 else None

        node_obj = Node(id=node_id, depends=external_deps, after=after)
        node_objects.append(node_obj)

    logger.debug(f"Converted {len(node_objects)} nodes to Node objects")

    # Use the new preference chain logic
    extended_dependencies = extend_nodes(node_objects)
    clusters = build_chains(extended_dependencies)

    logger.debug(f"Built {len(clusters)} chains")

    # Compute all possible resolution paths
    all_resolution_paths = list(compute_all_resolution_pathes(clusters))

    if not all_resolution_paths:
        # No valid resolution path found - this indicates a serious dependency issue
        node_ids = [node["id"] for node in nodes]
        error_msg = (
            f"No valid resolution path found for nodes: {node_ids}. "
            "This indicates circular dependencies or unsatisfiable constraints."
        )
        logger.error(error_msg)
        raise CircularDependencyError(error_msg)

    logger.debug(f"Found {len(all_resolution_paths)} resolution paths")

    # Sort paths by score (best score first)
    all_resolution_paths.sort(key=lambda path: -compute_path_score(list(path)))

    # Extract the final execution order from the best path
    best_path = all_resolution_paths[0]
    final_order = [node_id for chain in best_path for node_id in chain.ids]

    logger.debug(f"Best execution order: {final_order}")

    return final_order
