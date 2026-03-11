# pyscaf

A python uv scaffolder - A tool to quickly initialize Python projects with complete and modern configuration.

## Installation

### With pip

```bash
pip install open-pyscaf
```

### With uv (recommended)

[uv](https://docs.astral.sh/uv/) is a fast Python package manager. Install `pyscaf` as a global tool:

```bash
uv tool install open-pyscaf
```

Or run it directly without installing:

```bash
uvx open-pyscaf init --interactive my-project
```

Or add it to a project's dev dependencies:

```bash
uv add --dev open-pyscaf
```

### From the test repository

```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple open-pyscaf
```

Or with uv:

```bash
uv tool install open-pyscaf --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple
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

### 📦 Package Management with uv
- Complete `uv` configuration for package management
- Features similar to R's `DESCRIPTION` file
- Dependency management and publication

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

This project is developed to simplify Python project creation with integrated best practices from the start.


