import itertools
import logging
from typing import List

from pydantic import BaseModel

satisfied = set[str]()
executed = set[str]()

logger = logging.getLogger(__name__)


class Node(BaseModel):
    id: str
    depends: List[str] = []
    after: str | None = None

    @property
    def external_dependencies(self) -> set[str]:
        return set(self.depends) - (
            set([self.after]) if self.after is not None else set()
        )


class ExtendedNode(Node):
    referenced_by: set[str] = set()


class ChainLink(BaseModel):
    children: list[ExtendedNode]
    head: ExtendedNode
    tail: ExtendedNode

    @property
    def ids(self) -> list[str]:
        return [node.id for node in self.children]

    @property
    def external_dependencies(self) -> set[str]:
        return set().union(
            *[node.external_dependencies for node in self.children]
        ) - set(self.ids)

    @property
    def referenced_by(self) -> set[str]:
        return set().union(*[node.referenced_by for node in self.children])


def extend_nodes(tree: list[Node]) -> list[ExtendedNode]:
    extended_nodes: list[ExtendedNode] = []
    for node in tree:
        extended_nodes.append(
            ExtendedNode(id=node.id, depends=node.depends, after=node.after)
        )
    for node in extended_nodes:
        for id in node.depends:
            found_node = next((x for x in extended_nodes if x.id == id), None)
            if found_node:
                found_node.referenced_by.add(node.id)
    return extended_nodes


def update_chains(node: ExtendedNode, chains: list[ChainLink]):
    for chain in chains:
        # If the node is the after of a chain, append it to the chain
        # And set the after chain of the chain to the node's after
        if (
            chain.head is not None
            and node.id == chain.head.id  # node is at the head of the chain
            and node.referenced_by.issubset(
                chain.ids
            )  # all the nodes that reference the node are in the chain
            and (
                set(node.external_dependencies).issubset(
                    chain.external_dependencies
                )  # all the external dependencies of the node are in the chain's ones
                or len(chain.external_dependencies)
                == 0  # The chain has no external dependencies
            )
        ):
            logger.debug(f"HEAD updated chain {chain.ids} with {node.id}")
            chain.head = node
            chain.children.append(node)
            return chain
        # If the node has it's dependance fulffiled by a chain, append it to the chain
        # A node is fulfilled by a chain if all of it's dependencies are in the chain
        # Or if the chain has the same external dependencies as the node
        if (
            node.after is not None
            and node.after == chain.tail.id
            and set(node.external_dependencies).issubset(chain.external_dependencies)
            and len(chain.tail.referenced_by)
            <= 1  # The node is referenced by only one other node (after relation), or is a leaf node
        ):
            logger.debug(f"QUEUED updated chain {chain.ids} with {node.id}")
            chain.tail = node
            chain.children.append(node)
            return chain

    # If the node is not in a chain, create a new one
    chain = ChainLink(children=[node], head=node, tail=node)
    chains.append(chain)
    return chain


def merge_chains(chain: ChainLink, chains: list[ChainLink]) -> ChainLink:
    for other_chain in chains:
        if chain == other_chain:
            continue
        # * other_chain --after--> chain
        # If the chain is the after of a chain, append it to the chain
        # And set the after other_chain of the other_chain to the chain's after
        if (
            chain.tail.id == other_chain.head.id  # chain is at the head of the chain
            and chain.tail.referenced_by.issubset(
                other_chain.ids
            )  # all the chains that reference the chain are in the chain
            and (
                set(chain.external_dependencies).issubset(
                    other_chain.external_dependencies.union(set(other_chain.ids))
                )  # all the external dependencies of the chain are in the chain's ones
                or len(other_chain.external_dependencies)
                == 0  # The other_chain has no external dependencies
            )
        ):
            logger.debug(f"HEAD merged chain {chain.ids} with {other_chain.ids}")
            other_chain.head = chain.head
            other_chain.children.extend(chain.children)
            chains.remove(chain)
            return other_chain
        # * other_chain --after--> chain
        # If the chain has it's dependance fulffiled by a chain, append it to the chain
        # A chain is fulfilled by a other_chain if all of it's dependencies are in the chain
        # Or if the other_chain has the same external dependencies as the chain
        if (
            chain.head.after == other_chain.tail.id
            and set(chain.external_dependencies).issubset(
                other_chain.external_dependencies.union(set(other_chain.ids))
            )
            and len(other_chain.tail.referenced_by)
            <= 1  # The chain is referenced by only one other chain (after relation), or is a leaf chain
        ):
            logger.debug(f"QUEUED merged chain {other_chain.ids} with {chain.ids}\n")
            other_chain.tail = chain.tail
            other_chain.children.extend(chain.children)
            chains.remove(chain)
            return other_chain
    logger.debug(f"no merge for {chain.ids}")
    return chain


def build_chains(tree: list[ExtendedNode]) -> list[ChainLink]:
    chains: list[ChainLink] = []
    for node in tree:
        logger.debug(f"Processing node {node}")
        chain = update_chains(node, chains)
        logger.debug(f"Chain (before merging): {chain.ids}")
        chain = merge_chains(chain, chains)
        logger.debug(
            f"Chain: {chain.ids} referenced by {chain.referenced_by}"
            f"  depends on {chain.external_dependencies}\n"
        )

    return chains


def compute_all_resolution_pathes(chains: list[ChainLink]):
    all_pathes: list[list[ChainLink]] = [
        list(path) for path in itertools.permutations(chains)
    ]

    # Filter valid paths: check head dependencies and external dependencies
    valid_pathes: list[list[ChainLink]] = []
    for path in all_pathes:
        is_valid = True
        for i, chain in enumerate(path):
            # Get previous chains' ids
            previous_ids = (
                set().union(*(prev_chain.ids for prev_chain in path[:i]))
                if i > 0
                else set()
            )

            # Check head dependency
            if (
                i > 0
                and chain.head is not None
                and chain.head.after not in previous_ids
            ):
                print(
                    f"Path rejected: chain {chain.ids} head {chain.head.id} not in previous ids {previous_ids}"
                )
                is_valid = False
                break

            # Check external dependencies
            if i > 0 and not chain.external_dependencies.issubset(previous_ids):
                print(
                    f"Path rejected: chain {chain.ids} external deps {chain.external_dependencies} not in previous ids {previous_ids}"
                )
                is_valid = False
                break

        if is_valid:
            valid_pathes.append(path)

    return valid_pathes


def compute_path_score(path: list[ChainLink]):
    score = 0
    # Start from the second element (index 1) to the end
    for i in range(1, len(path)):
        chain = path[i]
        previous_chain = path[i - 1]

        # Check if chain.head.id is different from previous chain's queue.id
        if chain.head.after != previous_chain.tail.id:
            score -= 1

    return score
