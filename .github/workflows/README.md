# GitHub Actions Workflows

This directory contains GitHub Actions workflows for the Lomen project.

## Tests Workflow

The `tests.yml` workflow runs on pull requests to the `main` branch and when pushing to `main`. It:

1. Sets up Python 3.10
2. Installs dependencies using uv
3. Runs linting with ruff (with continue-on-error)
4. Runs tests with pytest and collects coverage
5. Uploads coverage reports to Codecov
6. Posts a comment with coverage information on PRs

### Codecov Token

The workflow requires a `CODECOV_TOKEN` secret to be set in the repository settings. This token can be obtained by signing up at [codecov.io](https://codecov.io) and adding your repository.

To add this secret:
1. Go to your repository on GitHub
2. Navigate to Settings > Secrets and variables > Actions
3. Click "New repository secret"
4. Add the name `CODECOV_TOKEN` and paste your Codecov token as the value