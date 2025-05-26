def best_execution_order(nodes):
    # Transform input into dictionaries for quick lookup
    node_map = {node['id']: node for node in nodes}
    all_ids = set(node_map.keys())

    # Compute reverse dependencies: who depends on what
    external_map = {node['id']: set(node.get('external', [])) for node in nodes}

    # Init sets
    satisfied = set()
    executed = set()
    execution_order = []
    violations = []

    while len(executed) < len(nodes):
        candidates = []
        for node in nodes:
            node_id = node['id']
            if node_id in executed:
                continue
            if all(dep in satisfied for dep in external_map[node_id]):
                candidates.append(node)

        if not candidates:
            # Cycle or unsatisfiable: pick the first remaining node (stable order)
            remaining = sorted([node for node in nodes if node['id'] not in executed], key=lambda n: n['id'])
            chosen = remaining[0]
            violations.append(chosen['id'])
        else:
            # Greedy: choose the one that contributes most new fulfilled deps
            chosen = max(
                candidates,
                key=lambda node: len(set(node['fullfilled']) - satisfied)
            )

        execution_order.append(chosen['id'])
        satisfied.update(chosen['fullfilled'])
        executed.add(chosen['id'])

    if violations:
        print(f"Warning: Circular or unsatisfiable dependencies for: {violations}")

    return execution_order


nodes = [
    {
        "id": "versionning",
        "fullfilled": ["github", "coverage", "pytest", "ci-pipeline", "versionning", "pre-commit", "github-actions"],
        "external": []
    },
    {
        "id": "jupyter",
        "fullfilled": ["jupyter", "jupyter-actions"],
        "external": ["github"]
    },
    {
        "id": "test",
        "fullfilled": ["test", "test-coverage", "test-report", "test-report-html", "test-report-json", "test-report-latex", "test-report-markdown", "github-action-test"],
        "external": ["versionning"]
    }
]

print(best_execution_order(nodes))