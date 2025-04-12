# Contributing to Lomen

We're excited that you're interested in contributing to Lomen! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## How to Contribute

### Reporting Bugs

- Check if the bug has already been reported in the Issues section
- Use the bug report template when creating a new issue
- Include detailed steps to reproduce the bug
- Include information about your environment (OS, Python version, etc.)

### Suggesting Features

- Check if the feature has already been suggested in the Issues section
- Use the feature request template when creating a new issue
- Clearly describe the feature and its expected behavior
- Explain why this feature would be useful to Lomen users

### Pull Requests

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Make your changes
4. Add or update tests for your changes
5. Ensure all tests pass
6. Ensure your code follows our style guidelines
7. Submit a pull request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/lomen.git
cd lomen

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## Code Style

We use the following tools to maintain code quality:

- [Ruff](https://github.com/astral-sh/ruff) for linting and formatting
- [Black](https://github.com/psf/black) for code formatting

You can run these tools locally:

```bash
# Run linter
ruff check .

# Format code
black .
```

## Testing

- Write tests for all new code
- Ensure your changes don't break existing tests
- Tests should be clear and easy to understand

## Documentation

- Update documentation for any changed functionality
- Document new features thoroughly
- Use clear, concise language

## License

By contributing to Lomen, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).

## Questions?

If you have any questions about contributing, feel free to open an issue or reach out to the maintainers.