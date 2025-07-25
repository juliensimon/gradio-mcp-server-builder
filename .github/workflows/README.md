# GitHub Actions Workflows

This directory contains GitHub Actions workflows for CI/CD automation.

## Workflows

### 1. CI (`ci.yml`)
**Triggers**: Push to main/master, Pull requests
**Purpose**: Fast feedback on code changes

**What it does**:
- Runs on Python 3.10, 3.11, 3.12, 3.13
- Installs development dependencies
- Runs pre-commit hooks (code formatting, linting)
- Runs fast tests only (excludes `tests/slow/`)
- Uploads test artifacts

**Duration**: ~5-10 minutes per Python version

### 2. Documentation (`docs.yml`)
**Triggers**: Push to main/master with changes to docs
**Purpose**: Auto-deploy documentation to GitHub Pages

**What it does**:
- Builds MkDocs documentation
- Deploys to GitHub Pages

## Artifacts

CI workflow uploads artifacts:
- Test results (`.pytest_cache/`)
- Log files (`log/`)
- Retention: 7 days
- Uses latest GitHub Actions (v4 for artifacts, v4 for cache)

## Configuration

### Python Versions
- **CI**: 3.10, 3.11, 3.12, 3.13 (matrix)
- **Docs**: 3.13 only

### Dependencies
- Uses `requirements-dev.txt` for all workflows
- Caches pip dependencies for faster builds

### Test Configuration
- **CI**: `pytest tests/ -v --ignore=tests/slow/`

## Local Development

For local development, use the scripts in the project root:
- `./run-slow-tests.sh` - Run slow tests locally
- `pre-commit run --all-files` - Run pre-commit hooks
- `python -m pytest tests/ -v --ignore=tests/slow/` - Run fast tests
