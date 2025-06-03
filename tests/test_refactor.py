"""Tests for the refactor command."""

import os
from pathlib import Path

import pytest
from typer.testing import CliRunner

# Skip all tests in this module if GEMINI_API_KEY is not set
pytestmark = pytest.mark.skipif(
    not os.environ.get("GEMINI_API_KEY"),
    reason="GEMINI_API_KEY environment variable not set"
)

# Import after setting up the skip condition
from app.cli import app as cli_app  # noqa: E402


@pytest.fixture(scope="session")
def sample_python_file(tmp_path_factory: Any) -> Path:
    """Return a sample Python file for testing."""
    temp_dir = tmp_path_factory.mktemp("sample_python")
    file_path = temp_dir / "sample.py"
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


def test_refactor_file_command(
    cli_runner: CliRunner, sample_python_file: Path, tmp_path: Path
) -> None:
    """Test the refactor file command with a sample file."""
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    print(f"Sample file path: {sample_python_file}")
    print(f"Output directory: {output_dir}")

    # For now, let's just test that the command runs without errors
    # and creates the output file
    cmd = [
        "refactor",
        "file",
        str(sample_python_file),
        "--output-dir",
        str(output_dir),
        "--apply",
    ]
    result = cli_runner.invoke(cli_app, cmd, catch_exceptions=False)

    # Print the command output for debugging
    print("\nCommand output:")
    print(result.output)

    # Check the output
    assert result.exit_code == 0, f"Command failed with output: {result.output}"

    # Check that the output contains the expected refactoring
    assert (
        "Refactored code saved to:" in result.output
        or "No significant issues found" in result.output
    ), "Expected refactoring output not found in command output"

    # Also check that the report was created
    report_files = list(output_dir.glob("**/refactor_report_*.json"))
    print(f"\nFound report files: {report_files}")
    assert len(report_files) > 0, "No refactoring report was created"


def test_refactor_apply(
    cli_runner: CliRunner, sample_python_file: Path, tmp_path: Path
) -> None:
    """Test the refactor apply flag."""
    output_dir = tmp_path / "refactored"

    # For now, let's just test that the command runs without errors
    # and creates the output directory
    cmd = [
        "refactor",
        "file",
        str(sample_python_file),
        "--apply",
        "--output-dir",
        str(output_dir),
    ]
    result = cli_runner.invoke(cli_app, cmd, catch_exceptions=False)

    # Check the output
    assert result.exit_code == 0
    assert output_dir.exists()
