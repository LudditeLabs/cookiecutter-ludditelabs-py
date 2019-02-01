import click

from {{ cookiecutter.package_name }} import __version__


@click.group(context_settings=dict(help_option_names=['-h', '--help']))
@click.version_option(version=__version__, message='%(version)s')
def cli():
    """{{ cookiecutter.project_title }}."""
    pass


# Register commands.
# NOTE: mark with noqa at the end of import to skip flake8 checks here.
# import {{ cookiecutter.package_name }}.pkg.cli  # noqa
