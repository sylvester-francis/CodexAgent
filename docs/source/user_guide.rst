.. _user_guide:

User Guide
=========

This guide provides detailed information on using CodexAgent's features.

Code Summarization
------------------

CodexAgent can generate high-level summaries of your codebase by analyzing Python and Markdown files.

.. code-block:: bash

    # Basic usage
    codexagent summarize run /path/to/your/repo

    # Save output to a file
    codexagent summarize run /path/to/your/repo --output summary.md

    # Include hidden files and directories
    codexagent summarize run /path/to/your/repo --include-hidden

Documentation Generation
------------------------

Automatically generate documentation for your Python code using AI.

### For a Single File

.. code-block:: bash

    # Basic usage
    codexagent docgen file /path/to/your/file.py

    # Specify output file
    codexagent docgen file /path/to/your/file.py --output docs/api.md

    # Custom docstring style (numpy, google, or rest)
    codexagent docgen file /path/to/your/file.py --style google

### For a Directory

.. code-block:: bash

    # Basic usage
    codexagent docgen dir /path/to/your/directory

    # Specify output directory
    codexagent docgen dir /path/to/your/directory --output-dir docs/api

    # Recursively process subdirectories
    codexagent docgen dir /path/to/your/directory --recursive

Code Refactoring
---------------

Get AI-powered refactoring suggestions and apply them to your code.

### Analyzing Code

.. code-block:: bash

    # Analyze a file and show issues
    codexagent refactor file /path/to/your/file.py

    # Analyze with specific rules
    codexagent refactor file /path/to/your/file.py --rules performance,readability

### Applying Refactoring

.. code-block:: bash

    # Apply refactoring suggestions
    codexagent refactor file /path/to/your/file.py --apply

    # Specify output directory for refactored files
    codexagent refactor file /path/to/your/file.py --apply --output-dir refactored

    # Preview changes without applying
    codexagent refactor file /path/to/your/file.py --preview

Configuration Options
--------------------

You can configure CodexAgent using environment variables or a configuration file.

### Environment Variables

- ``GEMINI_API_KEY``: Your Google Gemini API key (required)
- ``LOG_LEVEL``: Logging level (default: INFO)
- ``DEFAULT_DOC_STYLE``: Default docstring style (numpy, google, or rest)
- ``MAX_TOKENS``: Maximum number of tokens for AI responses (default: 2048)
- ``TEMPERATURE``: Controls randomness in AI responses (0.0 to 1.0, default: 0.7)

### Configuration File

Create a ``.codexagent.yaml`` file in your project root:

.. code-block:: yaml

    # .codexagent.yaml
    default:
      doc_style: numpy
      max_tokens: 2048
      temperature: 0.7
    
    # Project-specific settings
    your_project_name:
      doc_style: google
      max_tokens: 4096

Troubleshooting
--------------

### Common Issues

1. **API Key Not Found**
   - Ensure the ``GEMINI_API_KEY`` environment variable is set
   - Check for typos in the API key

2. **Rate Limiting**
   - The Gemini API has rate limits; if you hit them, wait before making more requests
   - Consider implementing caching for frequent requests

3. **Long Processing Times**
   - For large codebases, processing may take time
   - Use the ``--max-files`` option to limit the number of files processed

### Getting Help

If you encounter issues, please:

1. Check the logs for error messages
2. Search the `GitHub issues <https://github.com/sylvester-francis/CodexAgent/issues>`_
3. Open a new issue if your problem isn't already reported
