A python scaffolder powered by [Pixi](https://pixi.sh) - A tool to quickly initialize Python projects with complete and modern configuration.

## Installation

The `pyscaf` module is available on PyPI and can be installed with pip:

```bash
pip install open-pyscaf
```

Or from the test repository:

```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple open-pyscaf
```

## Usage

### Interactive Mode

The usage is simple and interactive:

```bash
pyscaf init --interactive project_name
```

This command initializes a project named `project_name` by asking you a few questions about the project nature.

### Command Line Arguments

You can also provide arguments directly on the command line to avoid interactive questions:

```bash
pyscaf init --interactive test-versioning --versionning --remote-url tada.github --no-install
```

This allows you to:
- Set project name: `test-versioning`
- Enable versioning: `--versionning`
- Set remote URL: `--remote-url tada.github`
- Skip installation: `--no-install`

## Features

In its current version, `pyscaf` automatically configures:

### 📦 Environment Management with Pixi
- Complete `pixi` configuration for environment and dependency management
- Multi-platform support (Linux, macOS, Windows)
- Fast and reproducible environments

### 🎯 Code Quality with Ruff
- Configuration and installation of `ruff` for code normalization
- Default configuration included
- Automatic VS Code configuration:
  - Automatic import sorting
  - Line length control
  - Automatic linting and formatting

### 📓 Jupyter Environment
- Installation of `jupyter` and its dependencies
- Automatic file system structuring
- Ready-to-use configuration for data analysis

### 🔄 Git Versioning
- Automatic Git repository initialization
- Appropriate `.gitignore` file configuration
- Version tracking setup

### 🧪 Automated Testing
- `pytest` configuration for unit tests
- `pytest-cov` integration for code coverage
- Ready-to-use test structure

## Development

This project uses [Pixi](https://pixi.sh) for development.

### Setup

1. Install Pixi if you haven't already:
   ```bash
   curl -fsSL https://pixi.sh/install.sh | bash
   ```

2. Clone the repository and initialize the environment:
   ```bash
   pixi install
   ```

### Tasks

You can run various development tasks using `pixi run`:

- **Run pyscaf:** `pixi run pyscaf`
- **Run tests:** `pixi run test`
- **Check linting:** `pixi run lint`
- **Format code:** `pixi run format`

For a full list of available tasks, run:
```bash
pixi task list
```

### Environments

The project defines two environments:
- `default`: Basic environment for running the tool.
- `dev`: Includes development tools like `pytest`, `ruff`, and `python-semantic-release`.

To run a task in the `dev` environment:
```bash
pixi run -e dev <task_name>
```


