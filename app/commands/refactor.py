# app/commands/refactor.py
import json
import os
from datetime import datetime
from typing import Dict, Optional

import typer

from app.agents.refactor_agent import refactor_file

app = typer.Typer(help="Refactor Python code to improve quality and maintainability")


def get_output_path(
    file_path: str,
    output_dir: Optional[str],
    suffix: str = ""
) -> str:
    """Generate output path for refactored file."""
    if not output_dir:
        return ""
    
    file_name = os.path.basename(file_path)
    name, ext = os.path.splitext(file_name)
    
    if suffix:
        new_name = f"{name}_{suffix}{ext}"
    else:
        new_name = f"{name}_refactored{ext}"
    
    # Create a similar directory structure in the output directory
    rel_path = os.path.relpath(file_path, os.getcwd())
    rel_dir = os.path.dirname(rel_path)
    
    output_path = os.path.join(output_dir, rel_dir, new_name)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    return output_path


def save_report(report: Dict, output_dir: str) -> str:
    """Save refactoring report to a JSON file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(output_dir, f"refactor_report_{timestamp}.json")
    
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    
    return report_path


@app.command()
def file(
    file_path: str = typer.Argument(
        ..., 
        help="Path to the Python file to refactor"
    ),
    output_dir: Optional[str] = typer.Option(
        None, 
        "--output-dir", 
        "-o", 
        help="Directory to save refactored files"
    ),
    apply: bool = typer.Option(
        False, 
        "--apply", 
        help="Apply the refactoring changes"
    ),
) -> None:
    """Refactor a single Python file."""
    if not os.path.isfile(file_path):
        typer.echo(f"Error: File '{file_path}' does not exist.", err=True)
        raise typer.Exit(1)
    
    output_path = None
    if apply and output_dir:
        output_path = get_output_path(file_path, output_dir)
    
    result = refactor_file(file_path, output_path)
    
    # Display results
    typer.echo(f"\n{'='*80}")
    typer.echo(f"Refactoring report for: {file_path}")
    typer.echo(f"{'='*80}")
    
    if result.get('error'):
        typer.echo(f"Error: {result['error']}", err=True)
        raise typer.Exit(1)
    
    if result['issues']:
        typer.echo("\nIssues found:")
        typer.echo("-" * 40)
        typer.echo(result['issues'])
        
        typer.echo("\nSuggestions:")
        typer.echo("-" * 40)
        typer.echo(result['suggestions'])
        
        if apply:
            if output_path:
                typer.echo(f"\nRefactored code saved to: {output_path}")
            else:
                typer.echo("\nRefactored code (not saved, use --apply to save):")
                typer.echo("-" * 40)
                typer.echo(result['refactored_code'])
    else:
        typer.echo("\nNo significant issues found. The code looks good!")
    
    # Save detailed report if output directory is specified
    if output_dir:
        report_path = save_report(result, output_dir)
        typer.echo(f"\nDetailed report saved to: {report_path}")


@app.command()
def dir(
    directory: str = typer.Argument(
        ..., 
        help="Path to the directory containing Python files to refactor"
    ),
    output_dir: Optional[str] = typer.Option(
        None, 
        "--output-dir", 
        "-o", 
        help="Directory to save refactored files"
    ),
    apply: bool = typer.Option(
        False, 
        "--apply", 
        help="Apply the refactoring changes"
    ),
    recursive: bool = typer.Option(
        True, 
        "--recursive/--no-recursive", 
        "-r/", 
        help="Search for Python files recursively"
    ),
) -> None:
    """Refactor all Python files in a directory."""
    if not os.path.isdir(directory):
        typer.echo(f"Error: Directory '{directory}' does not exist.", err=True)
        raise typer.Exit(1)
    
    # Find all Python files
    python_files = []
    if recursive:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    python_files.append(os.path.join(root, file))
    else:
        python_files = [
            os.path.join(directory, f) 
            for f in os.listdir(directory) 
            if f.endswith('.py') and os.path.isfile(os.path.join(directory, f))
        ]
    
    if not python_files:
        typer.echo("No Python files found in the specified directory.")
        return
    
    # Process each file
    all_results = []
    for i, file_path in enumerate(python_files, 1):
        typer.echo(f"\n[{i}/{len(python_files)}] Processing: {file_path}")
        
        output_path = None
        if apply and output_dir:
            output_path = get_output_path(file_path, output_dir)
        
        result = refactor_file(file_path, output_path)
        all_results.append(result)
        
        if result.get('error'):
            typer.echo(f"  Error: {result['error']}", err=True)
        else:
            issue_count = len(result['issues'].split('\n')) if result['issues'] else 0
            typer.echo(f"  Found {issue_count} potential issues")
            
            if apply and output_path:
                typer.echo(f"  Refactored code saved to: {output_path}")
    
    # Generate summary report
    total_issues = sum(
        len(result['issues'].split('\n')) 
        for result in all_results 
        if result.get('issues')
    )
    
    typer.echo("\n" + "="*80)
    typer.echo(f"Refactoring complete! Processed {len(python_files)} files.")
    typer.echo(f"Total issues found: {total_issues}")
    
    # Save detailed report if output directory is specified
    if output_dir:
        report = {
            'timestamp': datetime.now().isoformat(),
            'directory': directory,
            'files_processed': len(python_files),
            'total_issues': total_issues,
            'results': all_results
        }
        
        report_path = save_report(report, output_dir)
        typer.echo(f"\nDetailed report saved to: {report_path}")


if __name__ == "__main__":
    app()