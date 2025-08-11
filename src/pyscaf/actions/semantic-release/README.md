## Semantic Release Configuration

This action configures [python-semantic-release](https://python-semantic-release.readthedocs.io/) for automated versioning, changelog generation, and package publishing.

### Overview

Semantic release automates the process of:
- **Version management**: Automatically bump version numbers based on commit messages
- **Changelog generation**: Create detailed changelogs from conventional commits
- **Package publishing**: Deploy to PyPI (TestPyPI automatically, Production PyPI manually)
- **GitHub releases**: Create GitHub releases with assets

### Features

#### Automatic Configuration
Configures `pyproject.toml` with some default semantic-release settings


#### GitHub Workflows (when git_host is "github")
- **Release workflow**: Automatically triggers on pushes to main branch
- **Manual deploy workflow**: Allows manual deployment to production PyPI

#### Commit Convention
Uses [Conventional Commits](https://www.conventionalcommits.org/) format:
- `feat:` - New features (minor version bump)
- `fix:` - Bug fixes (patch version bump)
- `BREAKING CHANGE:` - Breaking changes (major version bump)
- `docs:`, `style:`, `refactor:`, `test:`, `chore:` - No version bump

### Prerequisites

- Git repository with versioning enabled
- GitHub repository (for workflows)
- PyPI credentials configured as GitHub secrets:
  - `TEST_PYPI_PASSWORD` for TestPyPI
  - `PYPI_PASSWORD` for Production PyPI

### Configuration

The action automatically configures:
```toml
[tool.semantic_release]
version_variables = ["src/your_project/__init__.py:__version__"]
upload_to_pypi = true
upload_to_release = true
branch = "main"

[tool.semantic_release.remote]
type = "github"  # or "gitlab"
```

### Usage

1. **Automatic releases**: Push conventional commits to main branch
2. **Manual deployment**: Use GitHub Actions "Manual Deploy to Production PyPI" workflow

### Resources

#### Official Documentation
- [python-semantic-release Documentation](https://python-semantic-release.readthedocs.io/)
- [Conventional Commits Specification](https://www.conventionalcommits.org/)

#### Related Tools
- [Commitizen](https://commitizen-tools.github.io/commitizen/) - Interactive commit creation
- [Semantic Release CLI](https://github.com/semantic-release/semantic-release) - JavaScript version
- [GitHub Actions for Python](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python)

#### Best Practices
- [Keep a Changelog](https://keepachangelog.com/) - Changelog format guidelines
- [Semantic Versioning](https://semver.org/) - Version numbering specification
- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/) - Git branching strategy

### Example Workflow

```bash
# Make changes
git add .
git commit -m "feat: add new feature"
git push origin main

# Automatic release happens on GitHub
# Package published to TestPyPI
# GitHub release created

# Manual deployment to Production PyPI via GitHub Actions
```
