# CodexAgent

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

CodexAgent is an AI-powered command-line tool for code analysis, documentation generation, and refactoring. It uses Google's Gemini AI to provide intelligent code analysis and suggestions.

## ✨ Features

- **Code Summarization**: Generate high-level summaries of code repositories
- **Documentation Generation**: Automatically generate documentation for Python code
- **Code Refactoring**: Get AI-powered refactoring suggestions and apply them
- **Linting & Formatting**: Integrated with flake8, ruff, and black for code quality
- **Testing**: Comprehensive test suite with pytest
- **CI/CD**: GitHub Actions workflow for testing and linting

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

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# With coverage report
pytest --cov=app --cov-report=term-missing

# Run specific test file
pytest tests/test_summarize.py -v
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
