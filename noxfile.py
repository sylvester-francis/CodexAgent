"""Nox configuration for automated testing and linting."""
import os
import shutil
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional

import nox

# Default Python version to use for all sessions
PYTHON_DEFAULT_VERSION = "3.10"
PYTHON_VERSIONS = ["3.8", "3.9", "3.10", "3.11"]

# Package information
PACKAGE = "app"

# Nox options
nox.options.stop_on_first_error = True
nox.options.reuse_existing_virtualenvs = True

# Directories that hold our source code and tests
SOURCE_DIRS = ["app", "tests", "noxfile.py"]
TEST_DIRS = ["tests"]

# Environment variables to pass to all sessions
ENV: Dict[str, str] = {
    "PYTHONUNBUFFERED": "1",
    "PYTHONDONTWRITEBYTECODE": "1",
    "PYTHONWARNINGS": "ignore",
    "PYTHONPATH": ".",
}


def install_dependencies(session: nox.Session, *deps: str) -> None:
    """Install dependencies in the session's virtual environment."""
    if not deps:
        return
    
    # Use --no-deps to avoid reinstalling packages that are already installed
    session.install("--upgrade", "pip", "setuptools", "wheel")
    session.install(*deps)


def install_package(session: nox.Session, editable: bool = True) -> None:
    """Install the package in the session's virtual environment."""
    if editable:
        session.install("-e", ".")
    else:
        session.install(".")


def run_black(session: nox.Session, check: bool = True) -> None:
    """Run black code formatter."""
    args = ["black", *SOURCE_DIRS]
    if check:
        args.extend(["--check", "--diff"])
    session.run(*args, external=True)


def run_isort(session: nox.Session, check: bool = True) -> None:
    """Run isort import sorter."""
    args = ["isort", *SOURCE_DIRS]
    if check:
        args.append("--check-only")
    session.run(*args, external=True)


def run_flake8(session: nox.Session) -> None:
    """Run flake8 linter."""
    session.run("flake8", *SOURCE_DIRS, external=True)


def run_mypy(session: nox.Session) -> None:
    """Run mypy type checker."""
    session.run("mypy", "--strict", "app")


def run_pytest(
    session: nox.Session,
    *args: str,
    coverage: bool = True,
    xdist: bool = True,
) -> None:
    """Run pytest with coverage and xdist by default."""
    pytest_args = ["pytest", "-v"]
    
    if xdist and shutil.which("python") == session.virtualenv.python:
        pytest_args.extend(["-n", "auto"])
    
    if coverage:
        pytest_args.extend(
            [
                "--cov=app",
                "--cov-report=term-missing",
                "--cov-report=xml",
                "--cov-fail-under=0",  # Don't fail if coverage is below a threshold
            ]
        )
    
    pytest_args.extend(args)
    session.run(*pytest_args, external=True)


def run_safety_checks(session: nox.Session) -> None:
    """Run safety checks for known vulnerabilities in dependencies."""
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "pip",
            "freeze",
            "--all",
            f">{requirements.name}",
            external=True,
            silent=True,
        )
        session.install("safety")
        session.run("safety", "check", f"--file={requirements.name}", "--full-report")


@nox.session(python=PYTHON_VERSIONS)
def test(session: nox.Session) -> None:
    """Run the test suite."""
    install_package(session, editable=True)
    install_dependencies(session, "pytest", "pytest-cov", "pytest-mock", "pytest-xdist")
    run_pytest(session, *session.posargs)


@nox.session(python=PYTHON_DEFAULT_VERSION)
def lint(session: nox.Session) -> None:
    """Run all linters and type checkers."""
    install_package(session, editable=True)
    install_dependencies(
        session,
        "black",
        "isort",
        "flake8",
        "flake8-docstrings",
        "flake8-import-order",
        "mypy",
        "types-requests",
    )
    
    run_black(session, check=True)
    run_isort(session, check=True)
    run_flake8(session)
    run_mypy(session)


@nox.session(python=PYTHON_DEFAULT_VERSION)
def format(session: nox.Session) -> None:
    """Auto-format code with black and isort."""
    install_dependencies(session, "black", "isort")
    run_black(session, check=False)
    run_isort(session, check=False)


@nox.session(python=PYTHON_DEFAULT_VERSION)
def safety(session: nox.Session) -> None:
    """Check for known vulnerabilities in dependencies."""
    run_safety_checks(session)


@nox.session(python=PYTHON_DEFAULT_VERSION)
def coverage(session: nox.Session) -> None:
    """Generate and display coverage report."""
    install_package(session, editable=True)
    install_dependencies(session, "coverage", "pytest-cov")
    
    if not os.path.exists(".coverage"):
        session.run("pytest", "--cov=app", "--cov-report=xml", *session.posargs)
    
    session.run("coverage", "report", "--show-missing")
    session.run("coverage", "html")
    session.run("coverage", "xml")


@nox.session(python=PYTHON_DEFAULT_VERSION)
def docs(session: nox.Session) -> None:
    """Build the documentation."""
    install_package(session, editable=True)
    install_dependencies(
        session,
        "sphinx",
        "sphinx-rtd-theme",
        "sphinx-autodoc-typehints",
        "myst-parser",
    )
    
    # Build the docs
    session.run("sphinx-build", "-b", "html", "docs/source", "docs/build/html")


@nox.session(python=PYTHON_DEFAULT_VERSION)
def build(session: nox.Session) -> None:
    """Build source and wheel distributions."""
    session.install("build", "twine")
    
    # Clean up previous builds
    for path in ["dist", "build", f"{PACKAGE}.egg-info"]:
        if os.path.exists(path):
            shutil.rmtree(path)
    
    # Build the package
    session.run("python", "-m", "build")
    
    # Check the built distribution
    session.run("twine", "check", "--strict", "dist/*")


@nox.session(python=PYTHON_DEFAULT_VERSION)
def release(session: nox.Session) -> None:
    """Release a new version to PyPI."""
    # Make sure we're on the main branch
    if session.posargs and session.posargs[0] == "--local":
        # Allow local testing of the release process
        session.log("Running in local mode - not checking git branch")
    else:
        # Check if we're on the main branch
        branch = (
            session.run("git", "rev-parse", "--abbrev-ref", "HEAD", silent=True)
            .strip()
            .decode("utf-8")
        )
        if branch != "main":
            session.error("Releases can only be made from the 'main' branch")
    
    # Make sure there are no uncommitted changes
    if session.run("git", "diff", "--exit-code", "--quiet", external=True, success_codes=[0, 1]).returncode:
        session.error("There are uncommitted changes")
    
    # Run tests and checks
    session.notify("lint")
    session.notify("test")
    session.notify("safety")
    
    # Build the package
    build(session)
    
    # Upload to PyPI
    if session.posargs and session.posargs[0] == "--test":
        # Upload to TestPyPI
        session.run("twine", "upload", "--repository-url", "https://test.pypi.org/legacy/", "dist/*")
    else:
        # Upload to PyPI
        session.run("twine", "upload", "dist/*")
    
    # Tag the release
    version = ""
    with open("pyproject.toml", "r") as f:
        for line in f:
            if line.startswith("version = "):
                version = line.split('"')[1]
                break
    
    if not version:
        session.error("Could not determine version from pyproject.toml")
    
    session.run("git", "tag", f"v{version}")
    session.run("git", "push", "--tags")


@nox.session(python=PYTHON_DEFAULT_VERSION)
def clean(session: nox.Session) -> None:
    """Clean up build artifacts and caches."""
    # Remove Python cache files
    session.run("find", ".", "-type", "f", "-name", "*.py[co]", "-delete", external=True)
    session.run("find", ".", "-type", "d", "-name", "__pycache__", "-exec", "rm", "-r", "{}", "+", external=True)
    
    # Remove build artifacts
    for path in ["build", "dist", "*.egg-info", ".pytest_cache", ".mypy_cache", ".coverage", "htmlcov"]:
        if os.path.exists(path):
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
    
    # Remove documentation build artifacts
    if os.path.exists("docs/build"):
        shutil.rmtree("docs/build")
