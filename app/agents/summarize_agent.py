# app/agents/summarize_agent.py
from app.llm.gemini import run_gemini

SUMMARIZE_PROMPT_TEMPLATE = """
You are a senior software engineer.
Summarize the purpose and structure of the following project:

Files:
{file_listing}

Code:
{code_snippets}
"""


def summarize_code(file_listing: str, code_snippets: str) -> str:
    prompt = SUMMARIZE_PROMPT_TEMPLATE.format(
        file_listing=file_listing, code_snippets=code_snippets
    )
    return run_gemini(prompt)
