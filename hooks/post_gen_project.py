import shutil
from pathlib import Path

ROOT_DIR = Path.cwd()
PACKAGE_DIR = ROOT_DIR / "src" / "{{ cookiecutter.project_slug }}"


if __name__ == "__main__":
    if "{{ cookiecutter.with_bitbucket_pipelines }}" != "y":
        (ROOT_DIR / "bitbucket-pipelines.yml").unlink()

    if "{{ cookiecutter.with_cli }}" != "y":
        (PACKAGE_DIR / "cli.py").unlink()
        (PACKAGE_DIR / "__main__.py").unlink()

    if "{{ cookiecutter.with_docs }}" != "y":
        shutil.rmtree(ROOT_DIR / "docs")

    if "{{ cookiecutter.license }}" == "No license":
        (ROOT_DIR / "LICENSE").unlink()
