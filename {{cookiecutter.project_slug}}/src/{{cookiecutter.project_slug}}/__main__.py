# ruff: noqa: F821, E402
import os

from dotenv import load_dotenv

load_dotenv(dotenv_path=os.environ.get("{{ cookiecutter.project_slug | upper }}_ENV_FILE"))

import logging
import logging.config

from {{ cookiecutter.project_slug }}.cli import {{ "cli_with_history" if cookiecutter.with_cli_history else "cli" }}

COMMON_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(message)s",
        },
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "{{ cookiecutter.project_slug }}": {"level": "INFO"},
    },
    "root": {"handlers": ["stdout"], "level": "ERROR"},
}


def run():
    logging.config.dictConfig(COMMON_CONFIG)
    {{ "cli_with_history" if cookiecutter.with_cli_history else "cli" }}()


if __name__ == "__main__":
    run()
