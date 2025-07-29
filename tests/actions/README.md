# Action Testing Framework

This directory contains the testing framework for pyscaf actions using YAML configuration files.

## Structure

```
tests/actions/
├── test_actions.py          # Main test runner
├── core/                    # Tests for core action
│   ├── test1.yaml
│   ├── test2.yaml
│   └── test3.yaml
├── documentation/           # Tests for documentation action
│   └── ...
├── git/                    # Tests for git action
│   └── ...
└── ...
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

To run all action tests:
```bash
pytest tests/actions/test_actions.py -v
```

To run tests for a specific action:
```bash
pytest tests/actions/test_actions.py -k "test1.yaml" -v
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

- `core/test1.yaml`: Basic file existence checks
- `core/test2.yaml`: Content verification checks
- `core/test3.yaml`: Negative checks (files that should not exist)
- `core/test_default.yaml`: Testing default behavior (no CLI arguments)
- `core/test_empty_args.yaml`: Testing with empty CLI arguments 