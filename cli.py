# cli.py
import typer
from app.commands import summarize

app = typer.Typer()

# Add sub-apps
app.add_typer(summarize.app, name="summarize")

if __name__ == "__main__":
    app()
