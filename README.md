# Python project template

[Cookiecutter](https://github.com/audreyr/cookiecutter)_ template for a python package.

## Features

* [Poetry](https://python-poetry.org/) for dependency management.
* Command line interface using [click](https://click.palletsprojects.com/).
* Application configurations using [pydantic 1.10](https://docs.pydantic.dev/1.10/).
* Testing with [pytest](https://docs.pytest.org/en/latest/).
* [Sphinx](http://sphinx-doc.org/) documentation with [ReadTheDocs](https://readthedocs.io/) theme.
* Bitbucket pipeline configuration support.
* Pre-commit hooks with [pre-commit](https://pre-commit.com/).
* Code quality with [ruff](https://github.com/charliermarsh/ruff) and
  [black](https://github.com/psf/black).

## Usage

Make sure `cookiecutter` is installed:

```shell
$ pip install cookiecutter
```

Now you can generate a project:
```shell
$ cookiecutter https://github.com/LudditeLabs/cookiecutter-ludditelabs-py
```

It will ask you a few questions and then generate a project in the current directory
with the name of your package name.

## What to do next

You may want to tune some parameters after the project is generated.

* **Requirements**: Update packages versions in the `pyproject.toml`.

* **Bitbucket pipeline**: Update or change docker image and `script` steps.

* **.gitignore**: Add more entries if required. Make sure you add to correct
  place. Consider use global ``.gitignore`` for system-specific files and local
  one only for project-specific files. This article can help to figure out:
  https://gist.github.com/subfuzion/db7f57fff2fb6998a16c.
