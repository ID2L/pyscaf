from typing import List, Optional
from pydantic import BaseModel, ValidationError
import yaml
from collections import defaultdict
from typing import Dict, Any, Set, Tuple

class RawDependency(BaseModel):
    id: str
    depends: Optional[List[str]] = None
    after: Optional[str] = None

def load_and_complete_dependencies(yaml_path: str) -> List[RawDependency]:
    """
    Load dependencies from a YAML file and complete the 'after' property if possible.
    Returns a list of RawDependency objects.
    """
    with open(yaml_path, 'r') as f:
        raw_dependencies = yaml.safe_load(f)

    dependencies = []
    for entry in raw_dependencies:
        try:
            dep = RawDependency(**entry)
        except ValidationError as e:
            print(f"Validation error for dependency '{entry.get('id', '?')}': {e}")
            continue
        # Complete 'after' if missing and only one 'depends'
        if dep.after is None:
            if dep.depends:
                if len(dep.depends) == 1:
                    dep.after = dep.depends[0]
                else:
                    print(f"WARNING: Dependency '{dep.id}' has multiple 'depends' but no 'after'.")
        dependencies.append(dep)
    return dependencies 

def build_dependency_tree(
    dependencies: list[RawDependency],
    root_id: str
) -> tuple[dict, set[str]]:
    """
    Build a dependency tree starting from root_id, following 'after' recursively.
    Returns a tuple (tree, extra_depends) where:
      - tree is a nested dict representing the after-chain
      - extra_depends is a set of ids that are depends but not in the after-chain
    """
    # Index dependencies by id for fast lookup
    dep_by_id: dict[str, RawDependency] = {dep.id: dep for dep in dependencies}
    # Reverse index: for each id, who has after == id ?
    after_targets: defaultdict[str, list[RawDependency]] = defaultdict(list)
    for dep in dependencies:
        if dep.after:
            after_targets[dep.after].append(dep)

    visited: set[str] = set()
    extra_depends: set[str] = set()

    def _build(current_id: str) -> dict:
        if current_id in visited:
            return {}  # Prevent cycles
        visited.add(current_id)
        children = {}
        for dep in after_targets.get(current_id, []):
            # Pour chaque dépendance qui cible current_id via after
            children[dep.id] = _build(dep.id)
            # Si plusieurs depends, on récupère les dépendances supplémentaires
            if dep.depends and len(dep.depends) > 1:
                for d in dep.depends:
                    if d != current_id:
                        extra_depends.add(d)
        return children

    tree = {root_id: _build(root_id)}
    return tree, extra_depends 