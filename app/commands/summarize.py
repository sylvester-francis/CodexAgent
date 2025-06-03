# app/commands/summarize.py
import os
from typing import List, Tuple

import typer

from app.agents.summarize_agent import summarize_code

app = typer.Typer()


def gather_repo_data(path: str) -> Tuple[str, str]:
    """Gather repository data including file listings and code snippets.
    
    Args:
        path: Path to the repository
        
    Returns:
        Tuple containing file listings and code snippets as strings
    """
    file_listing: List[str] = []
    code_snippets: List[str] = []

    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith((".py", ".md")):
                full_path = os.path.join(root, file)
                file_listing.append(full_path)
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        code_snippets.append(f.read())
                except (IOError, UnicodeDecodeError):
                    continue

    return "\n".join(file_listing), "\n".join(code_snippets[:3])


def summarize_repo(path: str) -> str:
    """Generate a summary of the repository at the given path.
    
    Args:
        path: Path to the repository
        
    Returns:
        A string containing the summary of the repository
    """
    files, snippets = gather_repo_data(path)
    return summarize_code(files, snippets)


@app.command()
def run(path: str = typer.Argument(..., help="Path to the repo")) -> None:
    """Summarize the given code repository.
    
    Args:
        path: Path to the repository to summarize
    """
    typer.echo(summarize_repo(path))
