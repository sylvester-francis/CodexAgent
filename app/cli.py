# cli.py
import typer

from app.commands import docgen, refactor, summarize

app = typer.Typer(help="CodexAgent - AI-powered code analysis and refactoring tool")

# Add sub-apps with help text split for line length
app.add_typer(
    summarize.app,
    name="summarize",
    help="Generate summaries of code repositories"
)
app.add_typer(
    docgen.app,
    name="docgen",
    help="Generate documentation for Python code"
)
app.add_typer(
    refactor.app,
    name="refactor",
    help="Refactor Python code to improve quality"
)

if __name__ == "__main__":
    app()
