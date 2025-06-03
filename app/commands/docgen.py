# app/commands/docgen.py
import os
from typing import Optional

import typer
from rich.console import Console

from ..agents.docgen_agent import document_file, document_directory

app = typer.Typer(help="Generate documentation for Python code")
console = Console()


def generate_docs(file_or_dir: str, output: str, style: str = "numpy") -> None:
    """Generate documentation for Python files.
    
    Args:
        file_or_dir: Path to a Python file or directory containing Python files
        output: Output file or directory path
        style: Documentation style (numpy, google, or rest)
    """
    try:
        if os.path.isfile(file_or_dir):
            doc = document_file(file_or_dir, style)
            with open(output, 'w', encoding='utf-8') as f:
                f.write(doc)
            console.print(f"[green]Documentation generated: {output}")
        elif os.path.isdir(file_or_dir):
            docs = document_directory(file_or_dir, style)
            os.makedirs(output, exist_ok=True)
            
            for file_path, doc in docs.items():
                rel_path = os.path.relpath(file_path, file_or_dir)
                output_path = os.path.join(output, f"{os.path.splitext(rel_path)[0]}.md")
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(doc)
                console.print(f"[green]Documentation generated: {output_path}")
        else:
            console.print(f"[red]Error: {file_or_dir} is not a valid file or directory")
            raise typer.Exit(1)
            
    except Exception as e:
        console.print(f"[red]Error generating documentation: {str(e)}")
        raise typer.Exit(1) from e


@app.command()
def file(
    file_path: str = typer.Argument(..., help="Path to the Python file to document"),
    output: str = typer.Option("docs", "--output", "-o", help="Output file path"),
    style: str = typer.Option("numpy", "--style", "-s", help="Docstring style (numpy, google, or rest)")
) -> None:
    """Generate documentation for a single Python file."""
    generate_docs(file_path, output, style)


@app.command()
def dir(
    directory: str = typer.Argument(..., help="Path to the directory containing Python files"),
    output: str = typer.Option("docs", "--output", "-o", help="Output directory"),
    style: str = typer.Option("numpy", "--style", "-s", help="Docstring style (numpy, google, or rest)")
) -> None:
    """Generate documentation for all Python files in a directory."""
    generate_docs(directory, output, style)


if __name__ == "__main__":
    app()