import os

from dotenv import dotenv_values, find_dotenv
from platformdirs import user_config_path

PKG_NAME = "{{ cookiecutter.project_slug }}"
PKG_AUTHOR = "{{ cookiecutter.author | slugify }}"
ENV_PREFIX = "{{ cookiecutter.settings_env_prefix }}_"
DOTENV_FILENAME = ".env"


def load_pkg_dotenv(
    filename: str = DOTENV_FILENAME,
    env_prefix: str = ENV_PREFIX,
    pkg_name: str = PKG_NAME,
    pkg_author: str = PKG_AUTHOR,
) -> None:
    """Load package specific dot-env file.

    This function loads dot-env files in the following order:

    1. ``~/.config/<PKG_NAME>/.env`` - dot-env file from the user-specific config
       directory. The path is platform-specific. For example, on Windows it's
       ::

           C:\Documents and Settings\<User>\Application Data\Local Settings\
              <PKG_AUTHOR>\<PKG_NAME>\.env

       This location can be disabled if set environment variable::

           <ENV_PREFIX>ENV_FILE_NOUSER=1

    2. ``<CWD>/.env`` - dot-env file in the current working directory (CWD) or
       (optionally) parent dirs. ``.env`` file is searched in the CWD and then in the
       parent dirs. The first found file is loaded.

       This file overrides values from the previous location.

       You can disable searching in the parent directories by setting
       environment variable::

           <ENV_PREFIX>ENV_FILE_CWDONLY=1

    3. Environment variables - Environment variables are loaded at the end and override
       all previous values.

    Args:
        filename: Dot-env filename.
        env_prefix: Package environment variables prefix.
        pkg_name: Package name.
        pkg_author: Package author.

    Notes:
        This function should be called before importing any packages used in the
        package to ensure the environment is populated correctly.
    """
    osenv = os.environ

    if osenv.get(f"{env_prefix}ENV_FILE_NOUSER") != "1":
        path = user_config_path(pkg_name, pkg_author) / filename
        env = dotenv_values(dotenv_path=path)
    else:
        env = {}

    cwd_only = osenv.get(f"{env_prefix}ENV_FILE_CWDONLY") == "1"
    path = filename if cwd_only else find_dotenv(usecwd=True)
    env.update(dotenv_values(dotenv_path=path))

    for k, v in env.items():
        if k not in osenv and v is not None:
            osenv[k] = v

