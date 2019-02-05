import click

from {{ cookiecutter.package_name }} import __version__
{% if cookiecutter.use_appconfig == 'y' -%}
from {{ cookiecutter.package_name }} import appconfig
{% endif %}

@click.group(context_settings=dict(help_option_names=['-h', '--help']))
@click.version_option(version=__version__, message='%(version)s')
@click.option('--config', '-c', type=click.Path(dir_okay=False, exists=True),
              help='Path to additional config file.')
@click.pass_context
def cli(ctx{% if cookiecutter.use_appconfig == 'y' %}, config{% endif %}):
    """{{ cookiecutter.project_title }}."""
    {% if cookiecutter.use_appconfig == 'y' -%}
    ctx.meta['config'] = appconfig.load(config)
    {% endif -%}
    pass


# Register commands.
# NOTE: mark with noqa at the end of import to skip flake8 checks here.
# import {{ cookiecutter.package_name }}.pkg.cli  # noqa
