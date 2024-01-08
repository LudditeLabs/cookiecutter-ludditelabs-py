import logging

import click

from {{ cookiecutter.project_slug }} import __version__


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
