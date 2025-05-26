from collections import defaultdict
from typing import Dict, Any, Set, Tuple
from .dependency_loader import RawDependency

class DependencyTreeWalker:
    def __init__(self, dependencies: list[RawDependency], root_id: str):
        self.dependencies = dependencies
        self.root_id = root_id
        self.tree = None
        self.external_depends = set()
        self.fullfilled_depends = set()
        self._build_tree()

    def _build_tree(self):
        dep_by_id: dict[str, RawDependency] = {dep.id: dep for dep in self.dependencies}
        after_targets: defaultdict[str, list[RawDependency]] = defaultdict(list)
        for dep in self.dependencies:
            if dep.after:
                after_targets[dep.after].append(dep)

        visited: set[str] = set()
        extra_depends: set[str] = set()

        def _build(current_id: str) -> dict:
            if current_id in visited:
                return {}
            visited.add(current_id)
            children = {}
            for dep in after_targets.get(current_id, []):
                children[dep.id] = _build(dep.id)
                if dep.depends and len(dep.depends) > 1:
                    for d in dep.depends:
                        if d != current_id:
                            extra_depends.add(d)
            return children

        self.tree = {self.root_id: _build(self.root_id)}
        self.external_depends = extra_depends
        self.fullfilled_depends = visited
        print(f"fulfilled_depends: {self.fullfilled_depends}")

    def print_tree(self):
        """
        Print the dependency tree in a graphical way (like the 'tree' utility).
        External dependencies (extra_depends) are shown in red.
        """
        RED = '\033[91m'
        GREEN = '\033[92m'
        RESET = '\033[0m'
        def _print_subtree(subtree, prefix="", is_last=True):
            items = list(subtree.items())
            for idx, (node, children) in enumerate(items):
                connector = "└── " if idx == len(items) - 1 else "├── "
                print(prefix + connector + node)
                if children:
                    extension = "    " if idx == len(items) - 1 else "│   "
                    _print_subtree(children, prefix + extension, is_last=(idx == len(items) - 1))
                # Afficher les dépendances externes à ce niveau
                if node in self.external_depends:
                    print(prefix + ("    " if idx == len(items) - 1 else "│   ") + f"{RED}{node} (external){RESET}")
        # Afficher l'arbre principal
        _print_subtree(self.tree)
        # Afficher les dépendances externes non affichées
        shown = set()
        def _collect_shown(subtree):
            for node, children in subtree.items():
                shown.add(node)
                _collect_shown(children)
        _collect_shown(self.tree)
        for ext in self.external_depends:
            if ext not in shown:
                print(f"{RED}{ext} (external){RESET}") 
        for internal in self.fullfilled_depends:
            print(f"{GREEN}{internal} (fullfilled){RESET}") 