.. _contributing:

Contributing
============

We welcome contributions to CodexAgent! Here's how you can help:

Ways to Contribute
------------------

- Report bugs
- Suggest new features
- Submit code changes
- Improve documentation
- Share examples of how you're using CodexAgent

Development Setup
----------------

1. Fork the repository on GitHub
2. Clone your fork locally:

   .. code-block:: bash

      git clone https://github.com/sylvester-francis/CodexAgent.git
      cd CodexAgent
      git remote add upstream https://github.com/sylvester-francis/CodexAgent.git

3. Set up a development environment:

   .. code-block:: bash

      python -m venv venv
      source venv/bin/activate  # On Windows: venv\Scripts\activate
      pip install -e ".[dev]"
      pre-commit install

4. Create a feature branch:

   .. code-block:: bash

      git checkout -b feature/your-feature-name

5. Make your changes and commit them with a descriptive message
6. Push your branch and open a pull request

Coding Standards
----------------

- Follow `PEP 8 <https://www.python.org/dev/peps/pep-0008/>`_ style guidelines
- Use type hints for all function signatures
- Write docstrings following the Google style guide
- Keep lines under 88 characters (Black's default)
- Run the following before committing:

  .. code-block:: bash

     black .
     isort .
     flake8
     mypy .
     pytest

Testing
-------

- Write tests for new features and bug fixes
- Run tests with ``pytest``
- Aim for good test coverage (currently at X%)

Documentation
-------------

- Update documentation when adding new features
- Follow the existing documentation style
- Build the docs locally to check for errors:

  .. code-block:: bash

     cd docs
     make html

Pull Request Process
--------------------

1. Ensure tests pass and coverage is maintained
2. Update the CHANGELOG.md with your changes
3. Reference any relevant issues in your PR description
4. Request a review from one of the maintainers

Code of Conduct
---------------

Please note that this project is released with a Contributor Code of Conduct.
By participating in this project you agree to abide by its terms.

Reporting Issues
---------------

When reporting issues, please include:

1. A clear description of the problem
2. Steps to reproduce the issue
3. Expected vs. actual behavior
4. Version of CodexAgent and Python
5. Any error messages or logs

Feature Requests
---------------

For feature requests, please:

1. Explain the problem you're trying to solve
2. Describe the proposed solution
3. Provide examples of how the feature would be used
