"""Tests for the summarize command."""
from pathlib import Path
from unittest.mock import patch, MagicMock

def test_summarize_command(cli_runner, sample_python_file, tmp_path):
    """Test the summarize command with a sample file."""
    with patch("app.agents.summarize_agent.run_gemini") as mock_run_gemini:
        # Mock the Gemini response
        mock_run_gemini.return_value = "This is a test summary"
        
        # Run the command
        result = cli_runner.invoke(
            app, 
            ["summarize", "run", str(sample_python_file.parent)],
            catch_exceptions=False
        )
        
        # Check the output
        assert result.exit_code == 0
        assert "This is a test summary" in result.output
        mock_run_gemini.assert_called_once()


def test_summarize_nonexistent_dir(cli_runner, tmp_path):
    """Test summarize with a non-existent directory."""
    non_existent_dir = tmp_path / "nonexistent"
    result = cli_runner.invoke(
        app,
        ["summarize", "run", str(non_existent_dir)],
        catch_exceptions=False
    )
    assert result.exit_code != 0
    assert "does not exist" in result.output
