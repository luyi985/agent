# Python packages, `__init__.py`, `__main__.py`, and `uv`

This guide explains how Python modules and packages work, how `__init__.py` and
`__main__.py` are used, and how to run this project with `uv`.

## 1. Modules and packages

A **module** is a Python file. For example:

```text
script.py
```

It can define functions, classes, and variables:

```python
# script.py
MESSAGE = "Hello"

def run():
    print(MESSAGE)
```

Importing the module loads and executes its top-level code once, then makes its
definitions available through the module object:

```python
import script

script.run()
print(script.MESSAGE)
```

A **package** is a directory containing related modules. With this project,
the package is under `src/`:

```text
agent/
├── pyproject.toml
├── docs/
└── src/
    └── agent/
        ├── __init__.py
        └── __main__.py
```

The `src` directory is the source root; the importable package is
`src/agent`, whose import name is `agent`.

Python searches for importable modules using its module search path, including
the active environment and the installed project. `uv run` makes the project
available in its environment, so imports such as `import agent` work when a
command is run through `uv`.

## 2. `__init__.py`

`__init__.py` is the package initialization module. It runs when the package is
imported:

```python
import agent
```

In this project, `src/agent/__init__.py` contains:

```python
def main() -> None:
    print("Hello from agent!")
```

That makes `agent.main` available:

```python
import agent

agent.main()
```

`__init__.py` is commonly used for a small public API, package metadata, or
lightweight initialization. Avoid putting expensive work or command-line
behavior there, because it runs during imports.

Modern Python can use namespace packages without `__init__.py`, but keeping an
explicit, usually minimal, `__init__.py` makes a regular package clear and
provides a natural place for package-level exports.

## 3. `__main__.py`

`__main__.py` is the package's executable entry point. When you run:

```bash
python -m agent
```

Python finds and executes `agent/__main__.py`. The file must be named exactly
`__main__.py`—not `__main__py`.

Example:

```python
# src/agent/__main__.py
def main() -> None:
    print("Hello from the package entry point!")


if __name__ == "__main__":
    main()
```

The `if` guard is true when the module is executed as a program. It is false
when the module is imported, which prevents the CLI from starting as a side
effect of an import.

You can also put the implementation in another module and keep
`__main__.py` small:

```python
# src/agent/script.py
def run() -> None:
    print("Running")

# src/agent/__main__.py
from .script import run


if __name__ == "__main__":
    run()
```

Because this project uses a `src` layout, run that package through the project
environment:

```bash
uv run python -m agent
```

After the project has been installed into the active environment, the plain
Python form also works:

```bash
python -m agent
```

## 4. Running a module or function

The `-m` option accepts a **module name**, not a function name:

```bash
python -m agent.__main__   # valid
python -m agent:main       # invalid
```

To run `run()` in `agent/script.py`, add an executable guard to that module and
run it through `uv`:

```bash
uv run python -m agent.script
```

For a one-off function call, use:

```bash
python -c "from agent.script import run; run()"
```

The `module:callable` form is used by tools that create or serve entry points;
it is not syntax understood by `python -m`:

```text
agent.script:run
```

## 5. CLI entry points in `pyproject.toml`

This project declares two console commands:

```toml
[project.scripts]
agent = "agent:main"
main = "agent.__main__:main"
```

Each value has this form:

```text
command-name = "importable.module:callable"
```

Therefore:

- `agent = "agent:main"` creates an `agent` command that calls `main()` from
  `agent/__init__.py`.
- `main = "agent.__main__:main"` creates a `main` command that calls `main()`
  from `agent/__main__.py`.

The callable should normally accept no required arguments. Use `argparse`,
Typer, or Click when the CLI needs options and positional arguments.

## 6. Using `uv`

From the project root—the directory containing `pyproject.toml`—use:

```bash
# Create or update the environment and lock dependencies
uv sync

# Run the package entry point
uv run python -m agent

# Run the declared console commands
uv run agent
uv run main
```

`uv run` uses the project's environment and ensures the project is available
to Python. After changing `pyproject.toml`, run `uv sync` again so the
environment and scripts are refreshed.

If you install the project in editable mode with another installer, the
equivalent is:

```bash
pip install -e .
agent
```

## 7. Common problems

### `No module named 'agent.__main__'`

Check all of the following:

1. The file is exactly `src/agent/__main__.py`.
2. The package is under the configured source root, `src/`.
3. You ran the command from the project root.
4. You ran `uv sync` after changing the project or entry points.

### A relative import fails

This works when the file is run as a module:

```python
from .script import run
```

Run it with:

```bash
uv run python -m agent
```

Running the file directly, for example `python src/agent/__main__.py`, can
fail because Python no longer treats it as part of the `agent` package.

### Circular imports

Avoid having `__init__.py` import `script.py` while `script.py` imports values
back from `__init__.py`. Put shared data or functions in a separate module,
such as `config.py`, and import that module from both places.
