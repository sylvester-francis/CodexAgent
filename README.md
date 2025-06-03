<div align="center">

# CodexAgent

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![YouTube Channel](https://img.shields.io/badge/Subscribe-YouTube-FF0000?style=flat&logo=youtube&logoColor=white)](https://www.youtube.com/@TechWithSyl?sub_confirmation=1)

</div>

CodexAgent is an AI-powered command-line tool for code analysis, documentation generation, and refactoring. It uses Google's Gemini AI to provide intelligent code analysis and suggestions.

## ✨ Features

- **Code Summarization**: Generate high-level summaries of code repositories
- **Documentation Generation**: Automatically generate documentation for Python code with multiple style support (numpy, google, rest)
- **Code Refactoring**: Get AI-powered refactoring suggestions and apply them with a single command
- **Code Analysis**: Detect code quality issues and get improvement suggestions
- **Linting & Formatting**: Integrated with flake8, ruff, and black for code quality
- **Testing**: Comprehensive test suite with pytest
- **CI/CD**: GitHub Actions workflow for testing and linting
- **Modern CLI**: User-friendly command-line interface with rich output

## 🎥 Watch & Learn

Check out our YouTube channel for tutorials and demos:

[![Watch on YouTube](https://img.shields.io/badge/Subscribe-TechWithSyl-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@TechWithSyl?sub_confirmation=1)

## 🆕 Recent Updates

- **Enhanced Documentation Generation**: Added support for multiple docstring styles
- **Improved Code Analysis**: Better detection of code quality issues
- **Refactoring Tools**: More reliable code refactoring with detailed reports
- **Bug Fixes**: Fixed various linting and formatting issues
- **Improved Error Handling**: Better error messages and user feedback

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- [Poetry](https://python-poetry.org/) (recommended) or pip
- [Google Gemini API Key](https://makersuite.google.com/)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sylvester-francis/CodexAgent.git
   cd CodexAgent
   ```

2. **Set up the environment**
   ```bash
   # Using Poetry (recommended)
   poetry install
   poetry shell
   
   # Or using pip
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # For development
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your Gemini API key
   ```

## 🛠️ Usage

### Basic Commands

**Show help:**
```bash
python cli.py --help
```

**Get version:**
```bash
python cli.py --version
```

## 🔍 Code Analysis

Analyze code quality and get suggestions:
```bash
python cli.py analyze /path/to/your/code
```

### Documentation Generation

**Single file with specific style (numpy/google/rest):**
```bash
python cli.py docgen file /path/to/your/file.py --style numpy
```

**Directory with custom output:**
```bash
python cli.py docgen dir /path/to/your/directory --output-dir ./docs
```

### Code Refactoring

**Analyze without changes:**
```bash
python cli.py refactor file /path/to/your/file.py
```

**Apply refactoring with backup:**
```bash
python cli.py refactor file /path/to/your/file.py --apply --output-dir ./refactored
```

### Repository Summary

Generate a summary of a code repository:
```bash
python cli.py summarize run /path/to/your/repo --output summary.md
```

### Summarize a Repository

```bash
python cli.py summarize run /path/to/your/repo
```

### Generate Documentation

**Single file:**
```bash
python cli.py docgen file /path/to/your/file.py
```

**Directory:**
```bash
python cli.py docgen dir /path/to/your/directory
```

### Refactor Code

**Analyze a file:**
```bash
python cli.py refactor file /path/to/your/file.py
```

**Apply refactoring:**
```bash
python cli.py refactor file /path/to/your/file.py --apply --output-dir ./refactored
```

## 🧪 Testing & Quality

Run the complete test suite:

```bash
# Run all tests with coverage
pytest --cov=app --cov-report=term-missing

# Run specific test file with verbose output
pytest tests/test_summarize.py -v

# Run all tests in parallel (requires pytest-xdist)
pytest -n auto

# Run linters
flake8 app tests
ruff check .

# Auto-fix linting issues
ruff check --fix .
ruff format .
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CodexAgent CLI Tool                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────────────────────┐    │
│  │             │     │             │     │                             │    │
│  │  Commands   │────▶│    Agents    │────▶│        LLM Backend          │    │
│  │  (CLI)      │     │  (Logic)     │     │    (Google Gemini API)      │    │
│  │             │     │             │     │                             │    │
│  └─────────────┘     └─────────────┘     └───────────────┬─────────────┘    │
│          │                     │                           │                  │
│          ▼                     ▼                           │                  │
│  ┌─────────────┐     ┌─────────────┐                     │                  │
│  │   Output    │     │  Utilities  │◀───────────────────┘                  │
│  │  Formatters │     │  (Helpers)  │                                       │
│  └─────────────┘     └─────────────┘                                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

```

### Component Interactions:

1. **CLI Commands**: Entry point for user interactions (summarize, docgen, refactor)
2. **Agents**: Core business logic for different functionalities
3. **LLM Backend**: Google Gemini API integration for AI capabilities
4. **Output Formatters**: Format results for console/file output
5. **Utilities**: Shared helper functions and common utilities

## Project Structure

```
CodexAgent/
├── app/                    # Main application package
│   ├── agents/             # AI agents for different tasks
│   │   ├── docgen_agent.py # Documentation generation
│   │   ├── refactor_agent.py # Code refactoring
│   │   └── summarize_agent.py # Code summarization
│   ├── commands/           # CLI command implementations
│   ├── llm/                # Language model integrations
│   └── utils/              # Utility functions
├── tests/                  # Test suite
├── .github/workflows/      # GitHub Actions workflows
├── .flake8                 # Flake8 configuration
├── .pre-commit-config.yaml # Pre-commit hooks
├── pyproject.toml          # Project metadata and dependencies
└── README.md               # This file
```

## 🧹 Linting and Formatting

```bash
# Run flake8
flake8 app tests

# Run ruff
ruff check .
ruff format --check .

# Auto-fix with ruff
ruff check --fix .
ruff format .
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Google Gemini](https://ai.google.dev/) - For the powerful AI models
- [Typer](https://typer.tiangolo.com/) - For the CLI framework
- [Pytest](https://docs.pytest.org/) - For testing framework
