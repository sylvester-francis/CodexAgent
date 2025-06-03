# app/agents/docgen_agent.py
from typing import Dict, List, Optional
from dataclasses import dataclass
import ast
import os
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
    methods: List[FunctionInfo]
    docstring: str
    source: str

def extract_functions_and_classes(code: str) -> Dict[str, List[FunctionInfo]]:
    """Extract functions and classes from Python source code."""
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
                
                functions.append(FunctionInfo(
                    name=node.name,
                    args=args,
                    returns=returns,
                    docstring=docstring,
                    source=source
                ))
        
        elif isinstance(node, ast.ClassDef):
            methods = []
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    args = [arg.arg for arg in item.args.args if arg.arg != 'self']
                    returns = ast.unparse(item.returns) if item.returns else None
                    docstring = ast.get_docstring(item) or ""
                    source = ast.unparse(item)
                    
                    methods.append(FunctionInfo(
                        name=item.name,
                        args=args,
                        returns=returns,
                        docstring=docstring,
                        source=source
                    ))
            
            docstring = ast.get_docstring(node) or ""
            source = ast.unparse(node)
            
            classes.append(ClassInfo(
                name=node.name,
                methods=methods,
                docstring=docstring,
                source=source
            ))
    
    return {
        'functions': functions,
        'classes': classes
    }

def generate_documentation(code_info: Dict, style: str = "numpy") -> str:
    """Generate documentation for the given code information."""
    prompt = f"""You are a technical documentation writer. Generate professional documentation for the following code.
    
Code Structure:
"""
    
    # Add functions
    if code_info['functions']:
        prompt += "\nFunctions:\n"
        for func in code_info['functions']:
            prompt += f"\nFunction: {func.name}({', '.join(func.args)})"
            if func.returns:
                prompt += f" -> {func.returns}"
            prompt += f"\nDocstring: {func.docstring}\n"
            prompt += f"Source: {func.source}\n"
    
    # Add classes
    if code_info['classes']:
        prompt += "\nClasses:\n"
        for cls in code_info['classes']:
            prompt += f"\nClass: {cls.name}\n"
            prompt += f"Docstring: {cls.docstring}\n"
            prompt += f"Source: {cls.source}\n"
            
            if cls.methods:
                prompt += "\nMethods:\n"
                for method in cls.methods:
                    prompt += f"\n  Method: {method.name}({', '.join(method.args)})"
                    if method.returns:
                        prompt += f" -> {method.returns}"
                    prompt += f"\n  Docstring: {method.docstring}\n"
                    prompt += f"  Source: {method.source}\n"
    
    prompt += f"\nPlease generate comprehensive documentation in {style} style. Include detailed descriptions, parameters, return values, and examples where appropriate.\n"
    
    return run_gemini(prompt)

def document_file(file_path: str, style: str = "numpy") -> str:
    """Generate documentation for a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
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
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                docs[file_path] = document_file(file_path, style)
    
    return docs