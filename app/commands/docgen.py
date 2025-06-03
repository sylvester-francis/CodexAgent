# app/commands/docgen.py
import typer
import os
from pathlib import Path
from typing import Optional
from app.agents.docgen_agent import document_file, document_directory

app = typer.Typer(help="Generate documentation for Python code")

@app.command()
def file(
    file_path: str = typer.Argument(..., help="Path to the Python file to document"),
    output: Optional[str] = typer.Option(
        None, "--output", "-o", help="Output file path (default: print to console)"
    ),
    style: str = typer.Option(
        "numpy", "--style", "-s", help="Docstring style (numpy, google, or rest)"
    ),
):
    """Generate documentation for a single Python file."""
    if not os.path.exists(file_path):
        typer.echo(f"Error: File '{file_path}' does not exist.", err=True)
        raise typer.Exit(1)
    
    documentation = document_file(file_path, style)
    
    if output:
        try:
            with open(output, 'w', encoding='utf-8') as f:
                f.write(documentation)
            typer.echo(f"Documentation written to {output}")
        except Exception as e:
            typer.echo(f"Error writing to {output}: {str(e)}", err=True)
            raise typer.Exit(1)
    else:
        typer.echo(documentation)

@app.command()
def dir(
    directory: str = typer.Argument(..., help="Path to the directory containing Python files"),
    output_dir: Optional[str] = typer.Option(
        None, "--output-dir", "-o", help="Output directory for documentation files"
    ),
    style: str = typer.Option(
        "numpy", "--style", "-s", help="Docstring style (numpy, google, or rest)"
    ),
):
    """Generate documentation for all Python files in a directory."""
    if not os.path.isdir(directory):
        typer.echo(f"Error: Directory '{directory}' does not exist.", err=True)
        raise typer.Exit(1)
    
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    docs = document_directory(directory, style)
    
    for file_path, documentation in docs.items():
        if output_dir:
            # Create a similar directory structure in the output directory
            rel_path = os.path.relpath(file_path, directory)
            output_path = os.path.join(output_dir, f"{os.path.splitext(rel_path)[0]}.md")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            try:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(documentation)
                typer.echo(f"Documentation written to {output_path}")
            except Exception as e:
                typer.echo(f"Error writing to {output_path}: {str(e)}", err=True)
        else:
            typer.echo(f"\n{'='*80}\nDocumentation for {file_path}\n{'='*80}")
            typer.echo(documentation)

if __name__ == "__main__":
    app()