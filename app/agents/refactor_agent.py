# app/agents/refactor_agent.py
import ast
import os
from dataclasses import dataclass
from typing import Dict, List, Optional

import astor  # type: ignore[import-untyped]

from app.llm.gemini import run_gemini


@dataclass
class CodeIssue:
    line: int = 0
    col: int = 0
    message: str = ""
    severity: str = "info"  # 'info', 'warning', 'error'
    suggestion: Optional[str] = None


def analyze_code_quality(code: str) -> List[CodeIssue]:
    """Analyze Python code for potential refactoring opportunities."""
    issues: List[CodeIssue] = []

    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return [
            CodeIssue(
                line=e.lineno or 0,
                col=e.offset or 0,
                message=f"Syntax error: {e.msg}",
                severity="error",
                suggestion=None,
            )
        ]

    # Check for common issues
    for node in ast.walk(tree):
        # Check for functions with too many arguments
        if isinstance(node, ast.FunctionDef):
            # Count non-self arguments
            arg_count = len(node.args.args)
            if node.args.vararg:
                arg_count += 1
            if node.args.kwarg:
                arg_count += 1

            if arg_count > 5:  # Arbitrary threshold
                issues.append(
                    CodeIssue(
                        line=node.lineno,
                        col=node.col_offset,
                        message=(
                            f"Function '{node.name}' has {arg_count} arguments, "
                            "which is too many. Consider refactoring."
                        ),
                        severity="warning",
                        suggestion=(
                            "Split into smaller functions or use a data class/"
                            "dictionary to group related arguments."
                        ),
                    )
                )

            # Check for long functions
            func_length = len(astor.to_source(node).split("\n"))
            if func_length > 50:  # Arbitrary threshold
                issues.append(
                    CodeIssue(
                        line=node.lineno,
                        col=node.col_offset,
                        message=(
                            f"Function '{node.name}' is {func_length} lines long. "
                            "Consider refactoring into smaller functions."
                        ),
                        severity="info",
                        suggestion=(
                            "Split this function into smaller, "
                            "single-responsibility functions."
                        ),
                    )
                )

    return issues


def get_refactoring_suggestions(code: str, issues: List[CodeIssue]) -> str:
    """Get refactoring suggestions for the given code and issues."""
    if not issues:
        return "No significant issues found. The code looks good!"

    # Format issues for the prompt
    issue_descriptions = []
    for i, issue in enumerate(issues, 1):
        desc = f"{i}. Line {issue.line}, Col {issue.col}: {issue.message}"
        if issue.suggestion:
            desc += f"\n   Suggestion: {issue.suggestion}"
        issue_descriptions.append(desc)

    prompt = (
        "You are an expert Python developer. Please provide refactoring suggestions "
        "for the following code based on the issues found. Focus on making the code "
        "more readable, maintainable, and Pythonic.\n\n"
        f"Code:\n```python\n{code}\n```\n\n"
        f"Issues found:\n" + "\n".join(issue_descriptions) + "\n\n"
        "Please provide your refactoring suggestions, including code snippets "
        "if applicable. Focus on the most important improvements first."
    )

    # Add type ignore since we can't modify the gemini module right now
    return run_gemini(prompt)  # type: ignore[no-any-return]


def apply_refactoring(code: str, suggestions: str) -> str:
    """Apply refactoring suggestions to the code."""
    prompt = (
        "You are an expert Python developer. Please refactor the following code "
        "based on the suggestions provided. Only return the refactored code, "
        "without any additional explanation.\n\n"
        f"Original code:\n```python\n{code}\n```\n\n"
        f"Refactoring suggestions:\n{suggestions}\n\n"
        "Please provide the refactored code that implements these suggestions:"
    )

    # Add type ignore since we can't modify the gemini module right now
    refactored_code = run_gemini(prompt)  # type: ignore[no-any-return]

    # Clean up the response to extract just the code block
    if "```python" in refactored_code:
        refactored_code = refactored_code.split("```python")[1].split("```")[0].strip()
    elif "```" in refactored_code:
        refactored_code = refactored_code.split("```")[1].split("```")[0].strip()

    return refactored_code, "Refactoring applied successfully"


def refactor_file(file_path: str, output_path: Optional[str] = None) -> Dict[str, str]:
    """Refactor a single Python file."""
    result: Dict[str, str] = {
        "original_file": file_path,
        "refactored_file": "",
        "report": "",
    }
    """Refactor a single Python file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()

        issues = analyze_code_quality(code)
        suggestions = get_refactoring_suggestions(code, issues)

        result = {
            "file": file_path,
            "issues": "\n".join(
                f"{issue.line}:{issue.col} [{issue.severity}] {issue.message}"
                for issue in issues
            ),
            "suggestions": suggestions,
            "refactored_code": None,
            "error": None,
        }

        if issues:
            refactored_code, _ = apply_refactoring(code, suggestions)
            result["refactored_code"] = refactored_code

            if output_path:
                output_dir = os.path.dirname(os.path.abspath(output_path))
                os.makedirs(output_dir, exist_ok=True)
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(refactored_code)

        return result
    except Exception as e:
        return {
            "file": file_path,
            "issues": "",
            "suggestions": "",
            "refactored_code": None,
            "error": str(e),
        }
