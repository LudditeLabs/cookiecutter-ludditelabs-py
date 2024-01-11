# {{ cookiecutter.project_title }}

{{ cookiecutter.project_short_description }}

## Installation

### Python environment

This project utilizes `poetry` as a dependency manager.
See [documentation on how to install it](https://python-poetry.org/docs/#installing-with-pipx).

You optionally can create `conda` or `mamba` environment for the project:
```shell
$ conda create -n {{ cookiecutter.project_slug }} python=3.10
$ conda active {{ cookiecutter.project_slug }} 
# Tell 'poetry' to use current python environment.
$ poetry config virtualenvs.prefer-active-python true
```

### Python packages

```shell
$ poetry install
$ poetry shell
{% if cookiecutter.with_cli == "y" -%}
$ {{ cookiecutter.project_slug | replace('_', '-') }} -h
{% endif -%}
```

If you want to run tests then run:
```shell
$ poetry install --with test
```

### Poetry issues

`poetry install` may fail with the `failed to unlock the collection` error.
This happens because of the 'keyring' feature.

You need to disable keyring usage to fix that.
You have the following options to disable keyring:

* Set env var `PYTHON_KEYRING_BACKEND` to disable keyring temporary:
  ```shell
  $ PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring poetry install
  
  # or
  $ export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring
  $ poetry install
  ````

* Disable keyring permanently:
  ```shell
  $ python -m keyring --disable
  ```
  
  or create `~/.config/python_keyring/keyringrc.cfg` with content:
  ```
  [backend]
  default-keyring=keyring.backends.null.Keyring
  ```

* Disable keyring permanently with `PYTHON_KEYRING_BACKEND`:
  Put `export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring` to `~/.bashrc`:
  ```shell
  $ echo 'export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring' >> ~/.bashrc
  $ source ~/.bashrc
  $ poetry install
  ```

For more information, see
[issue #1917](https://github.com/python-poetry/poetry/issues/1917).

{% if cookiecutter.with_cli == "y" -%}
## Application settings

By default, the application loads settings from the environment variables and
[dot-env](https://github.com/theskumar/python-dotenv) `.env` file located in the current working directory or its parents.

The application settings vars have prefix `{{ cookiecutter.settings_env_prefix }}_*`.

You can specify the path to the env file via `{{ cookiecutter.settings_env_prefix }}_ENV_FILE` variable:

```shell
$ {{ cookiecutter.settings_env_prefix }}_ENV_FILE=/path/to/dir/my.env {{ cookiecutter.project_slug | replace('_', '-') }} ... 
```

Hint: You can set this var in the `.bashrc`:

```shell
# ~/.bashrc
...
export {{ cookiecutter.settings_env_prefix }}_ENV_FILE=/path/to/dir/my.env
```

Example `.env` file:

```shell
{{ cookiecutter.settings_env_prefix }}_FOO=True
ANOTHER_PACKAGE_ENV_VAR=bar
```
{% endif -%}

## Development notes

### Development environment setup

```shell

$ poetry install --with test,dev
$ poetry shell
$ pre-commit install
```

### Code Style

This project is developed using [PEP8](https://www.python.org/dev/peps/pep-0008/)
style with the help of [ruff](https://github.com/charliermarsh/ruff).

If you don't use `pre-commit`, use the following command to check source code before
committing changes:
```shell
$ ruff check --fix .
$ ruff format .
```

Git commit messages follow these guidelines:
https://gist.github.com/robertpainsi/b632364184e70900af4ab688decf6f53.

### Packages

The project has several packages groups (dependencies groups):

* `main` - packages required to run the `{{ cookiecutter.project_slug }}`.
* `dev` - packages required for development.
* `test` - packages required for testing.
* `lint` - packages required for development.
* `doc` - packages required for documentation building.

Add packages to the project:
```shell
# Add to main.
$ poetry add <PKG>

# Add to GROUP.
$ poetry add -G <GROUP> <PKG>
```

For more info, see [poetry documentation](https://python-poetry.org/docs/managing-dependencies/#adding-a-dependency-to-a-group).

### Tests

Tests are located in the `tests/` directory and implemented with
[pytest](https://docs.pytest.org/en/latest/) framework.

You could run specific tests with `pytest` or all tests at once:
```shell
# Run all tests.
$ pytest tests

# Run single test case.
$ pytest tests/test_<name>.py

# Run tests with coverage report.
$ pytest --cov={{ cookiecutter.project_slug }} ...
```

See [pytest](https://docs.pytest.org/en/latest/) docs for more info.
