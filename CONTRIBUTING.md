# Contributing to Django App Store

First off, thank you for considering contributing to Django App Store! It's people like you that make this project such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps to reproduce the problem**
* **Provide specific examples**
* **Describe the behavior you observed and what you expected**
* **Include screenshots if possible**
* **Include your environment details** (OS, Python version, Django version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a detailed description of the suggested enhancement**
* **Explain why this enhancement would be useful**
* **List some examples of how it would be used**

### Pull Requests

* Fill in the required template
* Follow the Python/Django style guides
* Include appropriate test cases
* Update documentation as needed
* End all files with a newline

## Development Setup

1. Fork and clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements/development.txt`
5. Create a branch: `git checkout -b feature/your-feature-name`

## Style Guidelines

### Python Style Guide

* Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
* Use 4 spaces for indentation
* Maximum line length: 120 characters
* Use meaningful variable and function names

### Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line

### Testing

* Write tests for new features
* Ensure all tests pass before submitting PR
* Aim for high test coverage

## Project Structure

```
app-store/
├── accounts/           # User authentication
├── applications/       # App management
├── config/            # Project configuration
├── news/              # News system
├── utils/             # Utilities
└── tests/             # Test files
```

## Questions?

Feel free to open an issue or contact the maintainers.

Thank you for your contributions! 🎉

