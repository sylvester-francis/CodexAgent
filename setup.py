from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="codexagent",
    version="0.1.0",
    author="Sylvester Francis",
    author_email="techwithsyl@gmail.com",
    description="AI-powered code analysis, documentation, and refactoring tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sylvester-francis/CodexAgent",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "typer>=0.9.0",
        "python-dotenv>=1.0.0",
        "google-generativeai>=0.3.0",
        "astor>=0.8.1",
        "rich>=13.0.0",
    ],
    entry_points={
        "console_scripts": [
            "codexagent=app.cli:app",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
