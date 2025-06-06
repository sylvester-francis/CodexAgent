"""Pytest configuration and fixtures."""

import os
from pathlib import Path
from typing import Any, Generator

import pytest
from typer.testing import CliRunner


@pytest.fixture(scope="session")
def test_data_dir() -> Path:
    """Return the path to the test data directory."""
    return Path(__file__).parent / "data"


@pytest.fixture(scope="session")
def sample_python_file(test_data_dir: Path, tmp_path_factory: Any) -> Path:
    """Create a sample Python file for testing."""
    temp_dir = tmp_path_factory.mktemp("sample_python")
    file_path = temp_dir / "sample.py"
    # This function has several issues that should trigger refactoring:
    # 1. Too many arguments
    # 2. Long function
    # 3. Nested conditionals
    # 4. Hardcoded values
    file_path.write_text('''
def process_data(data, param1, param2, param3, param4, param5, param6):
    """Process data with many parameters."""
    result = {}
    for item in data:
        if item.get("active"):
            if item.get("type") == "A":
                result[item["id"]] = {
                    "value": item["value"] * 2,
                    "status": "processed"
                }
            elif item.get("type") == "B":
                result[item["id"]] = {
                    "value": item["value"] * 3,
                    "status": "processed"
                }
            else:
                result[item["id"]] = {
                    "value": item["value"],
                    "status": "unknown"
                }
    return result
''')
    return file_path


@pytest.fixture
def cli_runner() -> CliRunner:
    """Return a CliRunner for testing CLI commands."""
    return CliRunner()


@pytest.fixture(autouse=True)
def env_vars() -> Generator[None, None, None]:
    """Set up and clean up environment variables for testing."""
    # Save original environment
    original_env = os.environ.copy()
    
    # Set test environment variables
    os.environ["GEMINI_API_KEY"] = "test_key"
    os.environ["LOG_LEVEL"] = "DEBUG"
    
    yield  # Test runs here
    
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)
