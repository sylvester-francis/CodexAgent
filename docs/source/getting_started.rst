.. _getting_started:

Getting Started
==============

Installation
-----------

You can install CodexAgent using pip::

    pip install codexagent

Or for the latest development version::

    pip install git+https://github.com/sylvester-francis/CodexAgent.git

For development, you can install in editable mode with all dependencies::

    git clone https://github.com/sylvester-francis/CodexAgent.git
    cd CodexAgent
    pip install -e ".[dev]"

Basic Usage
-----------

CodexAgent provides a command-line interface for code analysis, documentation generation, and refactoring:

.. code-block:: bash

    # Summarize a codebase
    codexagent summarize run /path/to/your/repo

    # Generate documentation
    codexagent docgen file /path/to/your/file.py
    codexagent docgen dir /path/to/your/directory

    # Refactor code
    codexagent refactor file /path/to/your/file.py
    codexagent refactor file /path/to/your/file.py --apply --output-dir ./refactored

Configuration
------------

Create a `.env` file in your project root with your Gemini API key:

.. code-block:: bash

    # .env
    GEMINI_API_KEY=your_api_key_here
    LOG_LEVEL=INFO
    DEFAULT_DOC_STYLE=numpy  # Options: numpy, google, rest
