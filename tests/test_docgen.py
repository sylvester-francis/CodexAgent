"""Tests for the docgen command."""
from pathlib import Path
from unittest.mock import patch, MagicMock

def test_docgen_file_command(cli_runner, sample_python_file, tmp_path):
    """Test the docgen file command with a sample file."""
    output_file = tmp_path / "output.md"
    
    with patch("app.agents.docgen_agent.run_gemini") as mock_run_gemini:
        # Mock the Gemini response
        mock_run_gemini.return_value = "# Sample Documentation"
        
        # Run the command
        result = cli_runner.invoke(
            app,
            ["docgen", "file", str(sample_python_file), "--output", str(output_file)],
            catch_exceptions=False
        )
        
        # Check the output
        assert result.exit_code == 0
        assert "Documentation written to" in result.output
        assert output_file.exists()
        assert "# Sample Documentation" in output_file.read_text()


def test_docgen_dir_command(cli_runner, sample_python_file, tmp_path):
    """Test the docgen dir command with a sample directory."""
    output_dir = tmp_path / "docs"
    
    with patch("app.agents.docgen_agent.run_gemini") as mock_run_gemini:
        # Mock the Gemini response
        mock_run_gemini.return_value = "# Sample Documentation"
        
        # Run the command
        result = cli_runner.invoke(
            app,
            ["docgen", "dir", str(sample_python_file.parent), "--output-dir", str(output_dir)],
            catch_exceptions=False
        )
        
        # Check the output
        assert result.exit_code == 0
        assert "Documentation written to" in result.output
        assert (output_dir / "sample.md").exists()
