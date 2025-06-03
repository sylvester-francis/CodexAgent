.PHONY: install test lint format check-fmt check-types clean

# Install the package in development mode
install:
	pip install -e .[dev]
	pre-commit install

# Run tests
pytest:
	pytest -v --cov=app --cov-report=term-missing

test: pytest

# Lint the code
lint:
	ruff check .
	flake8 app tests

# Format the code
format:
	black .
	ruff check --fix .
	ruff format .

# Check formatting
check-fmt:
	black --check .
	ruff format --check .

# Check types
check-types:
	mypy app

# Clean up
clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -rf .cache

dev:
	uvicorn app.main:app --reload
