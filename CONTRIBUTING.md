# Development

## Environment

For local development, you need Python 3.11 or later installed.
We use [uv](https://docs.astral.sh/uv/) for project and environment management, and [just](https://github.com/casey/just) as our command runner.

## Dependencies

To install this package and its development dependencies, run:

```sh
just sync
```

or

```sh
uv sync --group dev
```

## Code checking

To execute all non-mutating code checking tools together, run:

```sh
just check
```

To display test coverage, run:

```sh
just coverage
```

### Linting

We utilize [ruff](https://docs.astral.sh/ruff/) for linting, which analyzes code for potential issues and enforces consistent style. Refer to `pyproject.toml` for configuration details.

To run linting:

```sh
just lint
```


### Formatting

[ruff](https://docs.astral.sh/ruff/) is also used for code formatting. Refer to `pyproject.toml` for configuration details.

To run formatting:

```sh
just format
```

## Testing

We use [pytest](https://docs.pytest.org/en/stable/) for testing. The default Python version is configured in `.python-version`; the local test matrix is configured in `.python-versions`.

```sh
# Run tests on the default Python version
uv run pytest -v

# Run tests across all supported Python versions
just test
```

## Pre-commit Hooks

We use [pre-commit](https://pre-commit.com/) to run quality checks automatically:

```sh
# Install pre-commit hooks
uv tool install pre-commit
pre-commit install

# Run hooks manually on all files
pre-commit run --all-files
```

## Documentation

We follow the [Google docstring format](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) for code documentation. All user-facing classes and functions must be documented with docstrings and type hints.
