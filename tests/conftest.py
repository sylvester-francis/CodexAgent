"""Pytest configuration and fixtures."""
import os
from pathlib import Path
from typing import Generator

import pytest
from typer.testing import CliRunner

from app.cli import app


@pytest.fixture(scope="session")
def test_data_dir() -> Path:
    """Return the path to the test data directory."""
    return Path(__file__).parent / "data"


@pytest.fixture(scope="session")
def sample_python_file(test_data_dir: Path, tmp_path_factory) -> Path:
    """Create a sample Python file for testing."""
    temp_dir = tmp_path_factory.mktemp("sample_python")
    file_path = temp_dir / "sample.py"
    file_path.write_text(
        'def hello(name: str = "world") -> str:\n    """Say hello to someone.\n    \n    Args:\n        name: Name to greet\n        \n    Returns:\n        A greeting message\n    """\n    return f"Hello, {name}!"\n'
    )
    return file_path


@pytest.fixture
def cli_runner() -> CliRunner:
    """Return a CliRunner for testing CLI commands."""
    return CliRunner()


@pytest.fixture(autouse=True)
env_vars() -> None:
    """Set up environment variables for testing."""
    os.environ["GEMINI_API_KEY"] = "test_key"
    yield
    # Cleanup if needed
    if "GEMINI_API_KEY" in os.environ:
        del os.environ["GEMINI_API_KEY"]
