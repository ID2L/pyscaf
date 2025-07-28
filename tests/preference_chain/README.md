# Preference Chain Integration Tests

This directory contains integration tests for the preference chain resolution mechanism.

## Test Structure

### Files Overview

- `test_preference_chain.py` - Main integration tests using YAML files
- `test_execution_order.py` - Tests for the `best_execution_order()` API function  
- `test_data/` - Directory containing YAML test cases
- `README.md` - This documentation

### Test Data Examples

The `test_data/` directory contains several YAML examples:

- `simple_example.yaml` - Basic linear dependency chain
- `diamond_example.yaml` - Diamond pattern (A -> B,C -> D)  
- `complex_example.yaml` - Real-world scenario with preferences

## Test Categories

### 1. YAML Integration Tests (`test_preference_chain.py`)

Tests the complete flow from YAML files to resolved execution order:

- **Simple linear chain**: A -> B -> C
- **Diamond dependencies**: Multiple paths converging  
- **Preference handling**: Using 'after' property for ordering preferences
- **Complex scenarios**: Real CI/CD pipeline-like dependencies
- **Error handling**: Circular dependency detection
- **Edge cases**: Single nodes, multiple roots

### 2. API Tests (`test_execution_order.py`)

Tests the `best_execution_order()` function directly:

- Input format: `[{"id": "name", "fullfilled": bool, "external": [deps]}]`
- Output: List of node IDs in optimal execution order
- Covers same dependency patterns as YAML tests
- Validates API contract and error handling

## Running Tests

```bash
# Run all preference chain tests
pytest tests/core/preference_chain/

# Run specific test file
pytest tests/core/preference_chain/test_preference_chain.py

# Run with debug logging
pytest tests/core/preference_chain/ -s --log-cli-level=DEBUG

# Run individual test
pytest tests/core/preference_chain/test_preference_chain.py::TestPreferenceChainIntegration::test_simple_linear_chain
```

## Adding New Test Cases

### YAML Test Cases

1. Create a new YAML file in `test_data/`:
```yaml
# my_test_case.yaml  
- id: node1
- id: node2
  depends: [node1]
- id: node3
  depends: [node2, node1]
  after: node2  # preference for ordering
```

2. Add a test method in `TestPreferenceChainIntegration`:
```python
def test_my_scenario(self, test_helper):
    test_helper.create_yaml_file("my_test_case.yaml", dependencies)
    result = test_helper.resolve_dependencies_from_yaml("my_test_case.yaml")
    
    # Validate expected ordering
    assert result[0] == "node1"
    # ... more assertions
```

### API Test Cases

Add test methods in `TestBestExecutionOrder`:
```python
def test_my_api_scenario(self):
    nodes = [
        {"id": "A", "fullfilled": False, "external": []},
        {"id": "B", "fullfilled": False, "external": ["A"]}
    ]
    result = best_execution_order(nodes)
    assert result == ["A", "B"]
```

## Test Helper Functions

### `PreferenceChainTestHelper`

- `resolve_dependencies_from_yaml(filename)` - Load YAML and resolve order
- `create_yaml_file(filename, dependencies)` - Create test YAML files

### Validation Patterns

Common patterns for validating results:

```python
# Check specific ordering
assert result == ["A", "B", "C"]

# Check relative ordering  
assert result.index("A") < result.index("B")

# Check first/last positions
assert result[0] == "root"
assert result[-1] == "final"

# Validate dependency constraints
for node in dependencies:
    node_index = result.index(node["id"])
    for dep in node.get("depends", []):
        dep_index = result.index(dep)
        assert dep_index < node_index, f"{dep} should come before {node['id']}"
```

## Key Concepts Tested

- **Dependencies**: `depends` field specifies required predecessors
- **Preferences**: `after` field specifies ordering preference when multiple options exist
- **Auto-completion**: Single dependencies automatically set 'after' preference
- **Chain building**: Groups of linearly dependent nodes  
- **Path scoring**: Algorithm selects optimal resolution path
- **Circular detection**: Invalid dependency cycles are caught and reported 