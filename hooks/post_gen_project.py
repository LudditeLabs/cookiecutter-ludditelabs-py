import shutil
from pathlib import Path

ROOT_DIR = Path.cwd()
PACKAGE_DIR = ROOT_DIR / "src" / "{{ cookiecutter.project_slug }}"


if __name__ == "__main__":
    if not {{ cookiecutter.with_bitbucket_pipelines }}:
        (ROOT_DIR / "bitbucket-pipelines.yml").unlink()

    if not {{ cookiecutter.with_cli }}:
        (PACKAGE_DIR / "cli.py").unlink()
        (PACKAGE_DIR / "__main__.py").unlink()
        (PACKAGE_DIR / "utils.py").unlink()
    elif not {{ cookiecutter.with_cli_history }}:
        (PACKAGE_DIR / "utils.py").unlink()

    if not {{ cookiecutter.with_docs }}:
        shutil.rmtree(ROOT_DIR / "docs")

    if "{{ cookiecutter.license }}" == "No license":
        (ROOT_DIR / "LICENSE").unlink()
