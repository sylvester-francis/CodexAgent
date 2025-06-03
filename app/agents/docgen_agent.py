# app/agents/docgen_agent.py
import ast
import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union, cast

import astor  # type: ignore[import-untyped]

from app.llm.gemini import run_gemini


@dataclass
class FunctionInfo:
    name: str
    args: List[str]
    returns: Optional[str]
    docstring: str
    source: str


@dataclass
class ClassInfo:
    name: str
    methods: List['FunctionInfo'] = field(default_factory=list)
    docstring: str = ""
    source: str = ""


def analyze_code(code: str) -> Dict[str, Any]:
    """Analyze Python code and extract information."""
    tree = ast.parse(code)

    functions = []
    classes = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Skip methods (they'll be processed as part of their class)
            if not any(isinstance(parent, ast.ClassDef) for parent in ast.walk(node)):
                args = [arg.arg for arg in node.args.args]
                returns = None
                if node.returns:
                    returns = ast.unparse(node.returns)

                docstring = ast.get_docstring(node) or ""
                source = ast.unparse(node)

                functions.append(
                    FunctionInfo(
                        name=node.name,
                        args=args,
                        returns=returns,
                        docstring=docstring,
                        source=source,
                    )
                )

        elif isinstance(node, ast.ClassDef):
            methods = []
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    args = [arg.arg for arg in item.args.args if arg.arg != "self"]
                    returns = ast.unparse(item.returns) if item.returns else None
                    docstring = ast.get_docstring(item) or ""
                    source = ast.unparse(item)

                    methods.append(
                        FunctionInfo(
                            name=item.name,
                            args=args,
                            returns=returns,
                            docstring=docstring,
                            source=source,
                        )
                    )

            docstring = ast.get_docstring(node) or ""
            source = ast.unparse(node)

            classes.append(
                ClassInfo(
                    name=node.name, methods=methods, docstring=docstring, source=source
                )
            )

    return {"functions": functions, "classes": classes}


def extract_functions_and_classes(code: str) -> Dict[str, Any]:
    """Extract functions and classes from the given code."""
    tree = ast.parse(code)

    functions = []
    classes = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Skip methods (they'll be processed as part of their class)
            if not any(isinstance(parent, ast.ClassDef) for parent in ast.walk(node)):
                args = [arg.arg for arg in node.args.args]
                returns = None
                if node.returns:
                    returns = ast.unparse(node.returns)

                docstring = ast.get_docstring(node) or ""
                source = ast.unparse(node)

                functions.append(
                    FunctionInfo(
                        name=node.name,
                        args=args,
                        returns=returns,
                        docstring=docstring,
                        source=source,
                    )
                )

        elif isinstance(node, ast.ClassDef):
            methods = []
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    args = [arg.arg for arg in item.args.args if arg.arg != "self"]
                    returns = ast.unparse(item.returns) if item.returns else None
                    docstring = ast.get_docstring(item) or ""
                    source = ast.unparse(item)

                    methods.append(
                        FunctionInfo(
                            name=item.name,
                            args=args,
                            returns=returns,
                            docstring=docstring,
                            source=source,
                        )
                    )

            docstring = ast.get_docstring(node) or ""
            source = ast.unparse(node)

            classes.append(
                ClassInfo(
                    name=node.name, methods=methods, docstring=docstring, source=source
                )
            )

    return {"functions": functions, "classes": classes}


def generate_documentation(code_info: Dict[str, Any], style: str = "numpy") -> str:
    """Generate documentation for the given code information.

    Args:
        code_info: Dictionary containing code structure information
        style: Documentation style to use (default: "numpy")

    Returns:
        str: Generated documentation
    """
    prompt = (
        "You are a technical documentation writer. Generate professional "
        "documentation for the following code.\n\n"
        "Code Structure:\n"
    )

    # Build the prompt with file structure
    tree = ast.parse(code_info["functions"][0].source)
    if isinstance(tree, ast.Module) and tree.body:
        for item in tree.body:
            if isinstance(item, ast.ClassDef):
                prompt += f"\nClass: {item.name}\n"
                if item.docstring:
                    prompt += f"  Docstring: {item.docstring}\n"

                # Add methods
                for method in item.body:
                    if not isinstance(method, ast.FunctionDef):
                        continue
                    prompt += f"\n  Method: {method.name}\n"
                    if method.docstring:
                        prompt += f"    Docstring: {method.docstring}\n"
                    # Add source code
                    source = astor.to_source(method).strip()
                    prompt += f"    Source: {source}\n"
            elif isinstance(item, ast.FunctionDef):
                prompt += f"\nFunction: {item.name}\n"
                if item.docstring:
                    prompt += f"  Docstring: {item.docstring}\n"
                # Add source code
                source = astor.to_source(item).strip()
                prompt += f"  Source: {source}\n"

    # Add documentation style instructions
    prompt += (
        f"\n\nPlease generate documentation in {style} style. "
        "Include detailed descriptions, parameters, return values, "
        "and examples where appropriate.\n"
    )

    # Call the Gemini API with the prompt and return the result
    return run_gemini(prompt)


def document_file(file_path: str, style: str = "numpy") -> str:
    """Generate documentation for a single file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()

        code_info = extract_functions_and_classes(code)
        return generate_documentation(code_info, style)
    except Exception as e:
        return f"Error processing {file_path}: {str(e)}"


def document_directory(directory: str, style: str = "numpy") -> Dict[str, str]:
    """Generate documentation for all Python files in a directory."""
    docs = {}

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                docs[file_path] = document_file(file_path, style)

    return docs
