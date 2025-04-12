# GitHub Actions Workflows

This directory contains GitHub Actions workflows for the Lomen project.

## Tests Workflow

The `tests.yml` workflow runs on pull requests to the `main` branch and when pushing to `main`. It:

1. Sets up Python 3.10
2. Installs dependencies using uv
3. Runs linting with ruff
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

## Testing Workflows Locally

You can test GitHub Actions workflows locally using [act](https://github.com/nektos/act). A script is provided to make this easy:

```bash
# Install act first
# macOS: brew install act
# Linux: Follow instructions at https://github.com/nektos/act#installation

# Run the test script without uploading to Codecov
./test-gh-actions.sh

# Run with your real Codecov token to test actual uploading
CODECOV_TOKEN=your_real_token ./test-gh-actions.sh
```

This will simulate a pull request to the main branch and run the tests workflow locally. Some GitHub-specific features like PR comments won't work locally, but it will help you verify that your workflow steps execute correctly.

### Notes for Local Testing

- The workflow has been configured to detect when it's running under `act` and will adapt accordingly
- GitHub-specific actions like creating PR comments will be skipped during local testing
- A special step will show the coverage report in the terminal instead
- By default, a dummy Codecov token is used, which means coverage won't actually be uploaded
- To test the actual Codecov upload, provide your real token as an environment variable: