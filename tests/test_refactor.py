"""Tests for the refactor command."""
from pathlib import Path
from unittest.mock import patch, MagicMock

def test_refactor_file_command(cli_runner, sample_python_file, tmp_path):
    """Test the refactor file command with a sample file."""
    with patch("app.agents.refactor_agent.run_gemini") as mock_run_gemini:
        # Mock the Gemini responses
        mock_run_gemini.side_effect = [
            "1:1 [info] Sample issue",  # analyze_code_quality
            "Sample refactoring suggestion",  # get_refactoring_suggestions
            "def hello(name: str = \"world\") -> str: return f\"Hello, {name}!\""  # apply_refactoring
        ]
        
        # Run the command
        result = cli_runner.invoke(
            app,
            ["refactor", "file", str(sample_python_file)],
            catch_exceptions=False
        )
        
        # Check the output
        assert result.exit_code == 0
        assert "Sample issue" in result.output
        assert "Sample refactoring suggestion" in result.output


def test_refactor_apply(cli_runner, sample_python_file, tmp_path):
    """Test the refactor apply flag."""
    output_dir = tmp_path / "refactored"
    
    with patch("app.agents.refactor_agent.run_gemini") as mock_run_gemini:
        # Mock the Gemini responses
        mock_run_gemini.side_effect = [
            "1:1 [info] Sample issue",
            "Sample refactoring suggestion",
            "def hello(name: str = \"world\") -> str: return f\"Hello, {name}!\""
        ]
        
        # Run the command with --apply
        result = cli_runner.invoke(
            app,
            ["refactor", "file", str(sample_python_file), "--apply", "--output-dir", str(output_dir)],
            catch_exceptions=False
        )
        
        # Check the output
        assert result.exit_code == 0
        assert "Refactored code saved to" in result.output
        
        # Check that the output file was created
        output_file = output_dir / sample_python_file.name
        assert output_file.exists()
