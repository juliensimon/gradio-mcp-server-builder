# GitHub Actions Workflows

This directory contains GitHub Actions workflows for CI/CD automation.

## Workflows

### 1. CI (`ci.yml`)
**Triggers**: Push to main/master, Pull requests
**Purpose**: Fast feedback on code changes

**What it does**:
- Runs on Python 3.9, 3.10, 3.11, 3.12
- Installs development dependencies
- Runs pre-commit hooks (code formatting, linting)
- Runs fast tests only (excludes `tests/slow/`)
- Uploads test artifacts

**Duration**: ~5-10 minutes per Python version

### 2. Slow Tests (`slow-tests.yml`)
**Triggers**:
- Manual trigger (workflow_dispatch)
- Weekly schedule (Sundays 2 AM UTC)
- Push to main/master with changes to:
  - `tests/slow/`
  - `input-samples/`
  - `source/`
  - `main.py`

**Purpose**: Comprehensive testing of server building and E2E scenarios

**What it does**:
- Runs on Python 3.12 only
- Runs all slow tests (server building, startup, E2E)
- 1-hour timeout
- Uploads test artifacts

**Duration**: ~30-60 minutes

### 3. Documentation (`docs.yml`)
**Triggers**: Push to main/master with changes to docs
**Purpose**: Auto-deploy documentation to GitHub Pages

**What it does**:
- Builds MkDocs documentation
- Deploys to GitHub Pages

## Manual Triggers

### Run Slow Tests Manually
1. Go to Actions tab in GitHub
2. Select "Slow Tests" workflow
3. Click "Run workflow"
4. Select branch and click "Run workflow"

## Artifacts

Both CI and slow test workflows upload artifacts:
- Test results (`.pytest_cache/`)
- Log files (`log/`)
- Retention: 7 days (CI), 30 days (slow tests)
- Uses latest GitHub Actions (v4 for artifacts, v4 for cache)

## Configuration

### Python Versions
- **CI**: 3.9, 3.10, 3.11, 3.12 (matrix)
- **Slow Tests**: 3.12 only
- **Docs**: 3.12 only

### Dependencies
- Uses `requirements-dev.txt` for all workflows
- Caches pip dependencies for faster builds

### Test Configuration
- **CI**: `pytest tests/ -v --ignore=tests/slow/`
- **Slow Tests**: `pytest tests/slow/ -v --timeout=600`

## Local Development

For local development, use the scripts in the project root:
- `./run-slow-tests.sh` - Run slow tests locally
- `pre-commit run --all-files` - Run pre-commit hooks
- `python -m pytest tests/ -v --ignore=tests/slow/` - Run fast tests
