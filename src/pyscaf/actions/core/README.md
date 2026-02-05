## Pixi Integration

This project uses Pixi for environment and dependency management. Pixi provides a modern, fast, and multi-platform way to manage project environments.

### Features

- **Environment Management**: Pixi manages project environments through `pyproject.toml`
- **Multi-platform support**: Works seamlessly on Linux, macOS, and Windows
- **Built-in Tasks**: Powerful task runner for development workflows
- **Fast and Reproducible**: Conda-based environment resolution

### Common Commands

```bash
# Install dependencies and setup environment
pixi install

# Run a task
pixi run <task_name>

# Add a new dependency
pixi add package-name

# Add a development dependency
pixi add --feature dev package-name

# List tasks
pixi task list

# Shell into the environment
pixi shell
```

### Project Structure

The project follows a modern structure:
- `pyproject.toml`: Project configuration, dependencies, and Pixi tasks
- `pixi.lock`: Locked dependencies for reproducible environments
- `src/`: Source code directory
- `tests/`: Test files directory

### Development

To start developing:
1. Ensure Pixi is installed: `curl -fsSL https://pixi.sh/install.sh | bash`
2. Run `pixi install` to initialize the environment
3. Start coding!

For more information, visit [Pixi's official documentation](https://pixi.sh).

## Ruff Integration

Ruff is an extremely fast Python linter and code formatter, written in Rust. It can replace Flake8, Black, isort, pyupgrade, and more, while being much faster than any individual tool.

### VSCode Default Configuration

The file `.vscode/default_settings.json` provides a recommended configuration for using Ruff in VSCode:

```json
{
    "[python]": {
      "editor.formatOnSave": true,
      "editor.codeActionsOnSave": {
        "source.fixAll": "explicit",
        "source.organizeImports": "explicit"
      },
      "editor.defaultFormatter": "charliermarsh.ruff"
    },
    "notebook.formatOnSave.enabled": true,
    "notebook.codeActionsOnSave": {
      "notebook.source.fixAll": "explicit",
      "notebook.source.organizeImports": "explicit"
    },
    "ruff.lineLength": 88
}
```

#### Explanation of each line:
- `editor.formatOnSave`: Enables automatic formatting on save for all files.
- `[python].editor.defaultFormatter`: Sets Ruff as the default formatter for Python files.
- `[python]editor.codeActionsOnSave.source.organizeImports`: Organizes Python imports automatically on save.
- `[python]editor.codeActionsOnSave.source.fixAll`: Applies all available code fixes (including linting) on save.
- `ruff.lineLength`: Line length for your python files

### Useful Ruff Commands

You can run the following commands commands directly in the shell

```bash
# Lint all Python files in the current directory
ruff check .

# Format all Python files in the current directory
ruff format .

# Automatically fix all auto-fixable problems
ruff check . --fix
```

For more information, see the [official Ruff VSCode extension documentation](https://github.com/astral-sh/ruff-vscode) and the [Ruff documentation](https://docs.astral.sh/ruff/). 

You can enable specific rules over a catalog of over 800+ rules, depending on your needs or framework of choice. Check it out at the [Ruff documentation](docs.astral.sh/ruff/rules/). 