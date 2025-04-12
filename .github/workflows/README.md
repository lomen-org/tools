# GitHub Workflows

This directory contains GitHub Actions workflows for the Lomen project.

## Workflows

### Tests (tests.yml)

Runs tests and linting on pull requests and pushes to the main branch.

- Runs on Python 3.10
- Uses `uv` for package management
- Runs linting with `ruff`
- Runs tests with `pytest` and collects coverage
- Uploads coverage to Codecov
- Comments coverage report on pull requests

### Publish to PyPI (publish.yml)

Publishes the package to PyPI when a new release is created or manually triggered.

- Triggered on release publish or workflow dispatch
- Optionally updates the version in pyproject.toml
- Builds the package using `build`
- Verifies the package with `twine`
- Publishes the package to PyPI using the PyPI API token

## Required Secrets

- `CODECOV_TOKEN`: Token for uploading coverage to Codecov
- `PYPI_API_TOKEN`: API token for publishing to PyPI