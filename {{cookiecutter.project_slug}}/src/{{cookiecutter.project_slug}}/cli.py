import logging
{%- if cookiecutter.with_cli_history %}
import os
import sys
from datetime import datetime
{%- endif %}

import click

from {{ cookiecutter.project_slug }} import __version__
{%- if cookiecutter.with_cli_history  %}
from {{ cookiecutter.project_slug }}.config import settings
from {{ cookiecutter.project_slug }}.utils import get_process_cmd


def cli_with_history():
    """Run CLI with saving info to the history file."""
    save_history()
    cli()


def save_history():
    """Save CLI command to the history file.

    History file entry format::

        [<TIMESTAMP>] [<CURRENT_WORKING_DIR>] COMMAND ARGS...
    """
    if settings.CLI_HISTORY:
        try:
            timestamp = datetime.now().isoformat()
            cmd = get_process_cmd()
            with settings.CLI_HISTORY_FILE.open("a", encoding="utf-8") as f:
                f.write(f"[{timestamp}] [{os.getcwd()}] {cmd}\n")
        except Exception as e:
            sys.stderr.write(f"ERROR SAVING TO HISTORY FILE: {e}\n\n")
{%- endif %}


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
@click.version_option(version=__version__, message="%(version)s")
@click.option("--verbose", "-v", is_flag=True, help="Verbose output.")
def cli(verbose):
    """{{ cookiecutter.project_title }}."""
    if verbose:
        logger = logging.getLogger("{{ cookiecutter.project_slug }}")
        logger.setLevel(logging.DEBUG)


# Register commands.
# NOTE: mark with noqa at the end of import to skip linter checks here.
#
# import {{ cookiecutter.project_slug }}.pkg.cli  # noqa
