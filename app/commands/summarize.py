# app/commands/summarize.py
import os

import typer

from app.agents.summarize_agent import summarize_code

app = typer.Typer()


def gather_repo_data(path: str):
    file_listing = []
    code_snippets = []

    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith((".py", ".md")):
                full_path = os.path.join(root, file)
                file_listing.append(full_path)
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        code_snippets.append(f.read())
                except Exception:
                    continue

    return "\n".join(file_listing), "\n".join(code_snippets[:3])


def summarize_repo(path: str) -> str:
    files, snippets = gather_repo_data(path)
    return summarize_code(files, snippets)


@app.command()
def run(path: str = typer.Argument(..., help="Path to the repo")):
    """Summarize the given code repository."""
    typer.echo(summarize_repo(path))
