# Action Testing Framework

This directory contains the testing framework for pyscaf actions using YAML configuration files.

## Structure

```
tests/actions/
├── conftest.py             # Pytest hooks for test filtering
├── test_actions.py         # Main test runner
├── core/                   # Tests for core action
│   ├── test_author.yaml
│   └── test_default.yaml
├── documentation/          # Tests for documentation action
│   └── ...
├── git/                   # Tests for git action
│   └── ...
└── ...                    # Other action tests
```

## YAML Configuration Format

Each test file should follow this structure:

```yaml
cli_arguments:  # Optional - can be omitted or empty to test default behavior
  action_name: true
  other_option: "value"
  flag_option: true

checks:
  - name: "Description of the check"
    type: exist | not_exist | contains | not_contains | custom
    file_path: "path/to/file"  # Required for file-based checks
    content: "text to search"   # Required for contains/not_contains
    function_path: "module:function"  # Required for custom checks
```

### Check Types

- **exist**: Verifies that a file exists at the specified path
- **not_exist**: Verifies that a file does not exist at the specified path
- **contains**: Verifies that a file contains the specified content
- **not_contains**: Verifies that a file does not contain the specified content
- **custom**: Executes a custom Python function for complex checks

### Custom Checks

For custom checks, the function should:
- Be importable from the specified module
- Accept a single argument (the temporary directory path)
- Return a boolean indicating success/failure

Example:
```python
# tests/actions/custom_checks.py
def check_project_structure(temp_dir):
    # Custom logic here
    return True
```

Then in YAML:
```yaml
checks:
  - name: "Custom structure check"
    type: custom
    function_path: "tests.actions.custom_checks:check_project_structure"
```

## Running Tests

### Using pytest with custom filtering (recommended)

The `conftest.py` in this directory provides custom pytest hooks for filtering tests by module and test name.

#### Run all action tests:
```bash
pytest tests/actions/ -v
```

#### Run tests for a specific module:
```bash
pytest tests/actions/ --action-filter="core" -v
```

#### Run a specific test:
```bash
pytest tests/actions/ --action-filter="core:test_author" -v
```

#### Run tests for multiple modules:
```bash
# Run core and documentation tests
pytest tests/actions/ --action-filter="core" -v
pytest tests/actions/ --action-filter="documentation" -v
```


## Adding New Tests

1. Create a new YAML file in the appropriate subdirectory
2. Define the CLI arguments for the action you want to test (optional)
3. Define the checks to verify the expected behavior
4. Run the tests to ensure they pass

### Test Types

- **Default behavior tests**: Omit `cli_arguments` or use empty `{}` to test default behavior
- **Specific argument tests**: Use `cli_arguments` with specific values to test different configurations
- **Negative tests**: Use `not_exist` and `not_contains` to verify files that should not be created

## Example Test Files

- `core/test_default.yaml`: Testing default behavior (no CLI arguments)
- `core/test_author.yaml`: Testing with specific CLI arguments (author)

## How It Works

### Test Execution Flow

1. **Discovery**: `discover_test_files()` scans YAML files in subdirectories
2. **Parametrization**: Tests are parametrized with `@pytest.mark.parametrize`
3. **Filtering**: The `conftest.py` hooks filter tests based on `--action-filter`
4. **Execution**: Each test creates a temporary directory and runs the pyscaf command
5. **Validation**: Checks verify the expected files and content

### Pytest Hooks

The `conftest.py` provides two main hooks:

- `pytest_addoption()`: Adds the `--action-filter` command-line option
- `pytest_collection_modifyitems()`: Filters test collection based on the filter option

This allows for efficient test execution by running only the tests you need during development. 