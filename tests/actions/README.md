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

### Using the utility script (recommended)

To run all action tests:
```bash
python tests/actions/run_tests.py
```

To run tests for a specific module:
```bash
python tests/actions/run_tests.py core
```

To run a specific test:
```bash
python tests/actions/run_tests.py core:test_author
```

### Using pytest directly

To run all action tests:
```bash
pytest tests/actions/test_actions.py -v
```

To run tests for a specific module:
```bash
PYSCAF_TEST_MODULE=core pytest tests/actions/test_actions.py -v
```

To run a specific test:
```bash
PYSCAF_TEST_NAME=test_author pytest tests/actions/test_actions.py -v
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