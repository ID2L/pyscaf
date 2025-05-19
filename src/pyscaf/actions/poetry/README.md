## Poetry Integration

This project uses Poetry for dependency management and packaging. Poetry provides a modern and efficient way to manage Python dependencies and build packages.

### Features

- **Dependency Management**: Poetry manages project dependencies through `pyproject.toml`
- **Virtual Environment**: Automatically creates and manages a virtual environment
- **Build System**: Integrated build system for creating Python packages
- **Lock File**: Generates a `poetry.lock` file for reproducible installations

### Common Commands

```bash
# Install dependencies
poetry install

# Add a new dependency
poetry add package-name

# Add a development dependency
poetry add --dev package-name

# Update dependencies
poetry update

# Run a command within the virtual environment
poetry run python script.py

# Activate the virtual environment
poetry shell
```

### Project Structure

The project follows a standard Python package structure:
- `pyproject.toml`: Project configuration and dependencies
- `poetry.lock`: Locked dependencies for reproducible builds
- `src/`: Source code directory
- `tests/`: Test files directory

### Development

To start developing:
1. Ensure Poetry is installed
2. Run `poetry install` to install all dependencies
3. Use `poetry shell` to activate the virtual environment
4. Start coding!

For more information, visit [Poetry's official documentation](https://python-poetry.org/docs/). 