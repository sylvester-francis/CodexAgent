"""Nox configuration for automated testing and linting."""

import os
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple, Union

import nox
from nox.sessions import Session

# Default Python version to use for all sessions
PYTHON_DEFAULT_VERSION: str = "3.10"
PYTHON_VERSIONS: List[str] = ["3.8", "3.9", "3.10", "3.11"]

# Package information
PACKAGE: str = "app"

# Nox options
nox.options.stop_on_first_error = True
nox.options.reuse_existing_virtualenvs = True

# Directories that hold our source code and tests
SOURCE_DIRS: List[str] = ["app", "tests", "noxfile.py"]
TEST_DIRS: List[str] = ["tests"]

# Environment variables to pass to all sessions
ENV: Dict[str, str] = {
    "PYTHONUNBUFFERED": "1",
    "PYTHONDONTWRITEBYTECODE": "1",
    "PYTHONWARNINGS": "ignore",
    "PYTHONPATH": ".",
}


def install_dependencies(session: Session, *deps: str) -> None:
    """Install dependencies in the session's virtual environment.
    
    Args:
        session: The nox session
        *deps: Dependencies to install
    """
    if not deps:
        return

    # Use --no-deps to avoid reinstalling packages that are already installed
    session.install("--upgrade", "pip", "setuptools", "wheel")
    session.install(*deps)


def install_package(session: Session, editable: bool = True) -> None:
    """Install the package in the session's virtual environment.
    
    Args:
        session: The nox session
        editable: Whether to install in editable mode
    """
    if editable:
        session.install("-e", ".")
    else:
        session.install(".")


def run_black(session: Session, check: bool = True) -> None:
    """Run black code formatter.
    
    Args:
        session: The nox session
        check: Whether to check formatting without making changes
    """
    args = ["black"]
    if check:
        args.append("--check")
    args.extend(SOURCE_DIRS)
    session.run(*args, external=True)


def run_isort(session: Session, check: bool = True) -> None:
    """Run isort import sorter.
    
    Args:
        session: The nox session
        check: Whether to check formatting without making changes
    """
    args = ["isort", "--profile", "black"]
    if check:
        args.append("--check-only")
    args.extend(SOURCE_DIRS)
    session.run(*args, external=True)


def run_flake8(session: Session) -> None:
    """Run flake8 linter.
    
    Args:
        session: The nox session
    """
    session.run("flake8", *SOURCE_DIRS, external=True)


def run_mypy(session: Session) -> None:
    """Run mypy type checker.
    
    Args:
        session: The nox session
    """
    session.run("mypy", "--strict", "--show-error-codes", "app")


def run_pytest(
    session: Session,
    *args: str,
    coverage: bool = True,
    xdist: bool = True,
) -> None:
    """Run pytest with coverage and xdist by default.
    
    Args:
        session: The nox session
        *args: Additional arguments to pass to pytest
        coverage: Whether to generate coverage reports
        xdist: Whether to use pytest-xdist for parallel test execution
    """
    pytest_args = ["pytest"]
    
    if coverage:
        pytest_args.extend(["--cov=app", "--cov-report=term-missing"])
    
    if xdist and "-n" not in args and "--numprocesses" not in args:
        pytest_args.extend(["-n", "auto"])
    
    pytest_args.extend(args)
    
    if not any(arg.startswith("tests/") for arg in args):
        pytest_args.extend(TEST_DIRS)
    
    session.run(*pytest_args, external=True)


def run_safety_checks(session: Session) -> None:
    """Run safety checks for known vulnerabilities in dependencies.
    
    Args:
        session: The nox session
    """
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
def test(session: Session) -> None:
    """Run the test suite.
    
    Args:
        session: The nox session
    """
    install_package(session, "pytest", "pytest-cov", "pytest-mock", "pytest-xdist")
    run_pytest(session, *session.posargs)


@nox.session(python=PYTHON_DEFAULT_VERSION)
def lint(session: Session) -> None:
    """Run all linters and type checkers.
    
    Args:
        session: The nox session
    """
    # Install all linting and type checking dependencies
    install_dependencies(
        session,
        "black",
        "isort",
        "flake8",
        "flake8-bugbear",
        "mypy",
        "types-setuptools",
    )

    # Run linters and type checkers
    run_isort(session)
    run_black(session)
    run_flake8(session)
    run_mypy(session)


@nox.session(python=PYTHON_DEFAULT_VERSION)
def format(session: Session) -> None:
    """Auto-format code with black and isort.
    
    Args:
        session: The nox session
    """
    install_dependencies(session, "black", "isort")
    run_black(session, check=False)
    run_isort(session, check=False)


@nox.session(python=PYTHON_DEFAULT_VERSION)
def safety(session: Session) -> None:
    """Check for known vulnerabilities in dependencies.
    
    Args:
        session: The nox session
    """
    install_dependencies(session, "safety")
    run_safety_checks(session)


@nox.session(python=PYTHON_DEFAULT_VERSION)
def coverage(session: Session) -> None:
    """Generate and display coverage report.
    
    Args:
        session: The nox session
    """
    install_package(session, "coverage", "pytest-cov")

    if not os.path.exists(".coverage"):
        session.run("pytest", "--cov=app", "--cov-report=xml", *session.posargs)

    session.run("coverage", "report", "--show-missing")
    session.run("coverage", "html")
    session.run("coverage", "xml")


@nox.session(python=PYTHON_DEFAULT_VERSION)
def docs(session: Session) -> None:
    """Build the documentation.
    
    Args:
        session: The nox session
    """
    install_package(session, "sphinx", "sphinx-rtd-theme", "myst-parser")
    
    # Build the docs
    session.run("sphinx-build", "-b", "html", "docs/source", "docs/build/html")


@nox.session(python=PYTHON_DEFAULT_VERSION)
def build(session: Session) -> None:
    """Build source and wheel distributions.
    
    Args:
        session: The nox session
    """
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
def release(session: Session) -> None:
    """Release a new version to PyPI.
    
    Args:
        session: The nox session
    """
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
    cmd = ["git", "diff", "--exit-code", "--quiet"]
    result = session.run(*cmd, external=True, success_codes=[0, 1], silent=True)
    if result.returncode != 0:
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
        session.run(
            "twine",
            "upload",
            "--repository-url",
            "https://test.pypi.org/legacy/",
            "dist/*",
        )
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
def clean(session: Session) -> None:
    """Clean up build artifacts and caches.
    
    Args:
        session: The nox session
    """
    # Remove Python cache files
    session.run(
        "find", ".", "-type", "f", "-name", "*.py[co]", "-delete", external=True
    )
    session.run(
        "find",
        ".",
        "-type",
        "d",
        "-name",
        "__pycache__",
        "-exec",
        "rm",
        "-r",
        "{}",
        "+",
        external=True,
    )

    # Remove build artifacts
    artifacts = [
        "build",
        "dist",
        "*.egg-info",
        ".pytest_cache",
        ".mypy_cache",
        ".coverage",
        "htmlcov",
        ".ruff_cache",
    ]

    for artifact in artifacts:
        if os.path.exists(artifact):
            if os.path.isdir(artifact):
                shutil.rmtree(artifact, ignore_errors=True)
            else:
                os.remove(artifact)

    # Remove .DS_Store files
    session.run("find", ".", "-name", ".DS_Store", "-delete", external=True)

    # Remove documentation build artifacts
    if os.path.exists("docs/build"):
        shutil.rmtree("docs/build")
