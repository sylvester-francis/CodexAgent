# app/agents/refactor_agent.py
from typing import Dict, List, Optional, Tuple
import ast
import astor
import os
from dataclasses import dataclass


@dataclass
class CodeIssue:
    line: int
    col: int
    message: str
    severity: str  # 'info', 'warning', 'error'
    suggestion: Optional[str] = None


def analyze_code_quality(code: str) -> List[CodeIssue]:
    """Analyze Python code for potential refactoring opportunities."""
    issues = []
    
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return [CodeIssue(
            line=e.lineno,
            col=e.offset,
            message=f"Syntax error: {e.msg}",
            severity="error"
        )]
    
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
                issues.append(CodeIssue(
                    line=node.lineno,
                    col=node.col_offset,
                    message=f"Function '{node.name}' has {arg_count} arguments, which is too many. Consider refactoring.",
                    severity="warning",
                    suggestion="Split into smaller functions or use a data class/dictionary to group related arguments."
                ))
            
            # Check for long functions
            func_length = len(astor.to_source(node).split('\n'))
            if func_length > 50:  # Arbitrary threshold
                issues.append(CodeIssue(
                    line=node.lineno,
                    col=node.col_offset,
                    message=f"Function '{node.name}' is {func_length} lines long. Consider refactoring into smaller functions.",
                    severity="info",
                    suggestion="Split this function into smaller, single-responsibility functions."
                ))
    
    return issues


def get_refactoring_suggestions(code: str, issues: List[CodeIssue]) -> str:
    """Get refactoring suggestions for the given code and issues."""
    if not issues:
        return "No significant issues found. The code looks good!"
    
    issues_text = "\n".join(
        f"- Line {issue.line}: [{issue.severity.upper()}] {issue.message}"
        f"{' Suggestion: ' + issue.suggestion if issue.suggestion else ''}"
        for issue in issues
    )
    
    prompt = f"""You are an expert Python developer. Please provide specific refactoring suggestions for the following code.
    
Code:
```python
{code}
```

Issues found:
{issues_text}

Please provide specific, actionable refactoring suggestions. For each suggestion:
1. Explain the issue in detail
2. Provide the refactored code
3. Explain why this is an improvement

Focus on:
- Improving readability
- Following Python best practices
- Making the code more maintainable
- Improving performance if applicable

Please format your response in Markdown with clear sections for each suggestion."""
    
    return run_gemini(prompt)


def apply_refactoring(code: str, suggestions: str) -> Tuple[str, str]:
    """Apply refactoring suggestions to the code."""
    prompt = f"""You are an expert Python developer. Please refactor the following code based on the instructions.
    
Original code:
```python
{code}
```

Instructions:
{suggestions}

Please provide the refactored code in a single code block. Only include the refactored code, no explanations or markdown formatting."""
    
    refactored_code = run_gemini(prompt)
    
    # Clean up the response to extract just the code block
    if '```python' in refactored_code:
        refactored_code = refactored_code.split('```python')[1].split('```')[0].strip()
    elif '```' in refactored_code:
        refactored_code = refactored_code.split('```')[1].split('```')[0].strip()
    
    return refactored_code, "Refactoring applied successfully"


def refactor_file(file_path: str, output_path: Optional[str] = None) -> Dict[str, str]:
    """Refactor a single Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        issues = analyze_code_quality(code)
        suggestions = get_refactoring_suggestions(code, issues)
        
        result = {
            'file': file_path,
            'issues': '\n'.join(f"{issue.line}:{issue.col} [{issue.severity}] {issue.message}" for issue in issues),
            'suggestions': suggestions,
            'refactored_code': None,
            'error': None
        }
        
        if issues:
            refactored_code, _ = apply_refactoring(code, suggestions)
            result['refactored_code'] = refactored_code
            
            if output_path:
                os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(refactored_code)
        
        return result
    except Exception as e:
        return {
            'file': file_path,
            'issues': '',
            'suggestions': '',
            'refactored_code': None,
            'error': str(e)
        }