# CodexAgent Documentation

This directory contains the source files for the CodexAgent documentation.

## Building the Documentation

### Prerequisites

- Python 3.8+
- pip
- Make (optional, but recommended)

### Installation

1. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Install the package in development mode from the project root:

   ```bash
   pip install -e .
   ```

### Building

To build the HTML documentation:

```bash
make html
```

The built documentation will be available in `build/html/`.

### Live Preview

For live preview with auto-reload:

```bash
make livehtml
```

Then open http://localhost:8000 in your browser.

## Documentation Structure

- `source/`: Source files for the documentation
  - `_static/`: Static files (CSS, images, etc.)
  - `_templates/`: Custom Sphinx templates
  - `*.rst`: ReStructuredText source files
  - `conf.py`: Sphinx configuration

## Writing Documentation

- Use reStructuredText (.rst) for documentation
- Follow the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) for docstrings
- Use MyST (Markedly Structured Text) for Markdown files

## Previewing Changes

To preview your changes:

1. Build the documentation:
   ```bash
   make html
   ```
2. Open `build/html/index.html` in your web browser

Or use the live preview:

```bash
make livehtml
```

## Documentation Deployment

The documentation is automatically deployed to Read the Docs when changes are pushed to the `main` branch.

## License

This documentation is licensed under the same terms as the main project.
