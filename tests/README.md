# Tests for pyscaf

This directory contains tests for the pyscaf project. The tests are organized into several categories:

- `test_cli.py`: Tests for the command-line interface
- `test_actions.py`: Tests for individual action classes
- `test_manager.py`: Tests for the action manager
- `test_interactive.py`: Tests for the interactive mode

## Running Tests

To run the tests, you can use the following commands:

```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=pyscaf

# Run specific test categories
pytest -m cli
pytest -m actions
pytest -m manager
pytest -m interactive

# Run tests in parallel
pytest -n auto
```

## Test Structure

The tests are organized as follows:

### CLI Tests
- Test version command
- Test project initialization for different project types
- Test interactive mode
- Test error handling

### Action Tests
- Test Poetry action
- Test Git action
- Test Jupyter action
- Test abstract base class

### Manager Tests
- Test package project creation
- Test notebook project creation
- Test mixed project creation
- Test project creation without versioning

### Interactive Tests
- Test package project configuration
- Test notebook project configuration
- Test mixed project configuration

## Test Fixtures

The tests use several fixtures:

- `runner`: A Click CLI runner for testing commands
- `temp_project_dir`: A temporary directory for project testing
- `project_config`: A test project configuration

## Best Practices

1. Use fixtures for common setup and teardown
2. Mock external dependencies
3. Test both success and failure cases
4. Keep tests focused and atomic
5. Use descriptive test names
6. Add comments for complex test scenarios 