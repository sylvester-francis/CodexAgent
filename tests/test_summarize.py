"""Tests for the summarize command."""

from unittest.mock import patch

from app.cli import app as cli_app


def test_summarize_command(cli_runner, sample_text_file, tmp_path):
    """Test the summarize command with a sample file."""
    output_file = tmp_path / "summary.txt"

    with patch("app.agents.summarize_agent.summarize_file") as mock_summarize:
        mock_summarize.return_value = "This is a test summary."

        result = cli_runner.invoke(
            cli_app, ["summarize", str(sample_text_file), "--output", str(output_file)]
        )

        assert result.exit_code == 0
        assert output_file.exists()


def test_summarize_nonexistent_dir(cli_runner, tmp_path):
    """Test the summarize command with a non-existent directory."""
    non_existent_dir = tmp_path / "nonexistent"
    output_file = tmp_path / "summary.txt"

    result = cli_runner.invoke(
        cli_app, ["summarize", str(non_existent_dir), "--output", str(output_file)]
    )

    # The command should exit with a non-zero status code
    assert result.exit_code != 0
    # The output should contain an error message
    assert "does not exist" in result.output.lower()
