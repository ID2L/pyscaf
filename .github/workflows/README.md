# GitHub Workflows Documentation

This repository uses a factorized workflow structure for automated deployment to PyPI.

## Workflow Structure

### 🔄 Reusable Workflow: `reusable-deploy.yml`
Core workflow containing the common deployment logic:
- **Semantic versioning** with python-semantic-release
- **Build artifacts** creation
- **GitHub releases** publication
- **PyPI deployment** with configurable target

### 🧪 Test Deployment: `deploy-test.yml`
- **Trigger**: Push to `develop` branch
- **Target**: TestPyPI (https://test.pypi.org/)
- **Secret**: `TEST_PYPI_PASSWORD`

### 🚀 Production Deployment: `deploy-production.yml`
- **Trigger**: Push to `main` branch
- **Target**: Production PyPI (https://pypi.org/)
- **Secret**: `PYPI_PASSWORD`

## Required Secrets

Make sure to configure these secrets in your GitHub repository settings:

1. **`PYPI_PASSWORD`**: Production PyPI API token or password
2. **`TEST_PYPI_PASSWORD`**: TestPyPI API token or password
3. **`GITHUB_TOKEN`**: Automatically provided by GitHub Actions

## Usage

1. **Development**: Push commits to `develop` → Automatic deployment to TestPyPI
2. **Release**: Push/merge to `main` → Automatic deployment to Production PyPI

## Benefits of This Structure

- ✅ **DRY Principle**: Single source of truth for deployment logic
- ✅ **Maintainability**: Changes only need to be made in one place
- ✅ **Flexibility**: Easy to add new environments or modify deployment targets
- ✅ **Clarity**: Separate workflows for different environments 