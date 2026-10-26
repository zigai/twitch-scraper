set positional-arguments
set script-interpreter := ['uv', 'run', '--no-project', '--', 'python']

_:
  @just help

_require-uv:
  @uv --version > /dev/null || (echo "Please install uv: https://docs.astral.sh/uv/" && exit 1)

# Check code style and potential issues
lint: _require-uv
  uv run --group dev ruff check .

# Format code
format: _require-uv
  uv run --group dev ruff format .

# Fix automatically fixable linting issues
fix: _require-uv
  uv run --group dev ruff check --fix .

# Run tests across all supported Python versions
[script]
test *args: _require-uv
  from pathlib import Path
  import os
  import shutil
  import subprocess
  import sys

  versions = [
      line.strip()
      for line in Path(".python-versions").read_text(encoding="utf-8").splitlines()
      if line.strip() and not line.lstrip().startswith("#")
  ]
  args = sys.argv[1:]
  if args[:1] == ["--"]:
      args = args[1:]

  def colorize(text):
      if os.environ.get("NO_COLOR"):
          return text
      if os.environ.get("FORCE_COLOR") or (sys.stdout.isatty() and os.environ.get("TERM") != "dumb"):
          return f"\033[1;36m{text}\033[0m"
      return text

  def print_separator(label):
      width = shutil.get_terminal_size(fallback=(120, 24)).columns
      text = f" {label} "
      if len(text) >= width:
          print(colorize(label), flush=True)
          return

      left = (width - len(text)) // 2
      right = width - len(text) - left
      print(colorize(f"{'─' * left}{text}{'─' * right}"), flush=True)

  def has_test_files():
      tests_dir = Path("tests")
      return tests_dir.exists() and any(
          path.is_file()
          for pattern in ("test_*.py", "*_test.py")
          for path in tests_dir.rglob(pattern)
      )

  if not args and not has_test_files():
      print("No tests found; skipping pytest.", flush=True)
      raise SystemExit(0)

  for py in versions:
      print_separator(f"Python {py}")
      result = subprocess.run([
          "uv",
          "run",
          "--python",
          py,
          "--isolated",
          "--group",
          "test",
          "--",
          "pytest",
          *args,
      ])
      if result.returncode:
          raise SystemExit(result.returncode)

# Build the package
build: _require-uv
  uv build

# Install the CLI executable to ~/.local/bin
install: _require-uv
  uv tool install --editable .

# Run the command-line interface
run *args: _require-uv
  uv run twitch-scraper {{args}}

# Setup or update local dev environment, keeps previously installed packages
setup: _require-uv
  uv sync --inexact --group dev
  uv run --group dev pre-commit install

# Run tests with coverage and show a coverage report
[script]
coverage: _require-uv
  from pathlib import Path
  import subprocess

  tests_dir = Path("tests")
  has_test_files = tests_dir.exists() and any(
      path.is_file()
      for pattern in ("test_*.py", "*_test.py")
      for path in tests_dir.rglob(pattern)
  )
  if not has_test_files:
      print("No tests found; skipping coverage.", flush=True)
      raise SystemExit(0)

  subprocess.run(["uv", "run", "coverage", "run", "-m", "pytest"], check=True)
  subprocess.run(["uv", "run", "coverage", "report"], check=True)

# Clean build artifacts and caches
clean:
  rm -rf .venv .pytest_cache .pyrefly .ruff_cache .mypy_cache
  find . -type d -name "__pycache__" -exec rm -r {} +

# Static type check with pyrefly
typecheck: _require-uv
  uv run --group dev pyrefly check --min-severity warn

# Check code for common misspellings
spell: _require-uv
  uv run --group dev codespell

# Run all non-mutating quality checks
check: lint test typecheck spell
  uv run --group dev ruff format --check .

# List available commands
help:
  @just --list

alias fmt := format
alias cov := coverage
