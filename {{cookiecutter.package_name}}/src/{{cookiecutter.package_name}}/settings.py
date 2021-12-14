from pathlib import Path
from dynaconf import Dynaconf


def load(*args):
    """Load app settings.

    Args:
        args: Path to files with extra settings.

    Returns:
        Settings object.
    """
    settings_files = [
        str(Path("~/.settings.{{ cookiecutter.package_name }}.yml").expanduser())
    ]
    settings_files.extend(args)
    return Dynaconf(
        envvar_prefix="{{ cookiecutter.package_name | upper }}",
        settings_files=settings_files,
    )
