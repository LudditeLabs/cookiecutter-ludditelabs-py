import click

from {{ cookiecutter.package_name }} import __version__
from {{ cookiecutter.package_name }} import settings


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
@click.version_option(version=__version__, message="%(version)s")
@click.option(
    "--config",
    "-c",
    type=click.Path(dir_okay=False, exists=True),
    help="Path to additional config file.")
@click.pass_context
def cli(ctx, config):
    """{{ cookiecutter.project_title }}."""
    ctx.meta["config"] = settings.load(config)


# Register commands.
# NOTE: mark with noqa at the end of import to skip flake8 checks here.
# import {{ cookiecutter.package_name }}.pkg.cli  # noqa
