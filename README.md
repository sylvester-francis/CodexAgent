# CodexAgent

CodexAgent is an AI-powered command-line tool for code analysis, documentation generation, and refactoring. It uses Google's Gemini AI to provide intelligent code analysis and suggestions.

## Features

- **Code Summarization**: Generate high-level summaries of code repositories
- **Documentation Generation**: Automatically generate documentation for Python code
- **Code Refactoring**: Get AI-powered refactoring suggestions and apply them

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/CodexAgent.git
   cd CodexAgent
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your Gemini API key:
   - Get an API key from [Google AI Studio](https://makersuite.google.com/)
   - Create a `.env` file in the project root and add your API key:
     ```
     GEMINI_API_KEY=your_api_key_here
     ```

## Usage

### Summarize a Repository

```bash
python cli.py summarize /path/to/your/repo
```

### Generate Documentation

For a single file:
```bash
python cli.py docgen file /path/to/your/file.py
```

For all Python files in a directory:
```bash
python cli.py docgen dir /path/to/your/directory
```

### Refactor Code

Analyze a file:
```bash
python cli.py refactor file /path/to/your/file.py
```

Refactor a file (apply changes):
```bash
python cli.py refactor file /path/to/your/file.py --apply --output-dir ./refactored
```

Refactor all Python files in a directory:
```bash
python cli.py refactor dir /path/to/your/directory --apply --output-dir ./refactored
```

## Available Commands

### Summarize

- `summarize <path>`: Generate a summary of the code repository

### Docgen

- `docgen file <file_path>`: Generate documentation for a single file
- `docgen dir <directory_path>`: Generate documentation for all Python files in a directory

### Refactor

- `refactor file <file_path>`: Analyze a file for refactoring opportunities
- `refactor dir <directory_path>`: Analyze all Python files in a directory

## Options

### Docgen Options

- `--output, -o`: Output file or directory for documentation
- `--style, -s`: Documentation style (numpy, google, or rest)

### Refactor Options

- `--output-dir, -o`: Directory to save refactored files
- `--apply, -a`: Apply the refactoring (save changes)
- `--recursive/--no-recursive, -r/`: Search for Python files recursively (default: True)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
