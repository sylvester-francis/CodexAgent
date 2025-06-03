# Contributing to CodexAgent

Thank you for your interest in contributing to CodexAgent! We appreciate your time and effort in making this project better. This document outlines the process for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Submitting a Pull Request](#submitting-a-pull-request)
- [Reporting Issues](#reporting-issues)
- [Code Style](#code-style)
- [Testing](#testing)
- [Documentation](#documentation)


## Getting Started

1. **Fork the repository** on GitHub.
2. **Clone your fork** of the repository:
   ```bash
   git clone https://github.com/sylvester-francis/CodexAgent.git
   cd CodexAgent
   ```
3. **Set up your development environment** (see below).

## Development Setup

### Prerequisites

- Python 3.8+
- [Poetry](https://python-poetry.org/) (recommended) or pip
- [Git](https://git-scm.com/)

### Installation

1. **Set up a virtual environment** (recommended):
   ```bash
   # Using venv
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Or using Poetry
   poetry install
   poetry shell
   ```

2. **Install dependencies**:
   ```bash
   # Using pip
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   
   # Or using Poetry (installs both main and dev dependencies)
   poetry install
   ```

3. **Set up pre-commit hooks**:
   ```bash
   pre-commit install
   ```

## Making Changes

1. **Create a new branch** for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-number-short-description
   ```

2. **Make your changes** following the [Code Style](#code-style) guidelines.

3. **Run tests** to ensure nothing is broken:
   ```bash
   pytest
   ```

4. **Commit your changes** with a descriptive commit message:
   ```bash
   git add .
   git commit -m "Add feature: short description of changes"
   ```
   
   Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification for commit messages.

5. **Push your changes** to your fork:
   ```bash
   git push origin your-branch-name
   ```

## Submitting a Pull Request

1. **Open a Pull Request** from your fork to the main repository's `main` branch.
2. **Describe your changes** in the PR description:
   - What changes were made?
   - Why were these changes necessary?
   - Any additional context or considerations?
3. **Reference any related issues** using keywords like "Closes #123" or "Fixes #456".
4. **Ensure all tests pass** and the code meets the project's standards.
5. **Request a review** from one or more maintainers.

## Reporting Issues

If you find a bug or have a feature request, please open an issue on GitHub with the following information:

1. **A clear title** describing the issue or feature request.
2. **A detailed description** of the problem or feature.
3. **Steps to reproduce** (for bugs) or **use cases** (for features).
4. **Expected vs. actual behavior** (for bugs).
5. **Screenshots or logs** (if applicable).
6. **Environment information** (OS, Python version, etc.).

## Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code.
- Use [Google-style docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) for documentation.
- Keep lines under 88 characters (Black's default).
- Use type hints for all function signatures and public APIs.
- Run the following commands to ensure code style consistency:
  ```bash
  # Auto-format code
  make format
  
  # Check code style
  make lint
  ```

## Testing

- Write tests for all new features and bug fixes.
- Ensure all tests pass before submitting a PR.
- Use descriptive test function names (e.g., `test_function_name_expected_behavior`).
- Run tests with:
  ```bash
  pytest
  
  # With coverage report
  pytest --cov=app --cov-report=term-missing
  ```

## Documentation

- Update the README.md and any relevant documentation when making changes.
- Add docstrings to all public functions, classes, and methods.
- Include examples in docstrings where helpful.

## Code Review Process

1. A maintainer will review your PR as soon as possible.
2. You may be asked to make changes or provide additional information.
3. Once approved, a maintainer will merge your PR.

## Thank You!

Your contributions are greatly appreciated. Thank you for helping to improve CodexAgent!
