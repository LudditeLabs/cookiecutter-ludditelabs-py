from {{ cookiecutter.package_name }}.utils.config import create_config


# Define UPPER_CASE attributes.
class DefaultAppConfig:
    """Default application's configuration."""

    #: Example config.
    EXAMPLE_CONF = 'hello'


def load(*args):
    """Load application configurations.

    Args:
        args: Configuration sources.

    Returns:
        Dict with loaded configurations.
    """
    defaults = [
        DefaultAppConfig,
        '~/.{{ cookiecutter.package_name.replace("_", "-") }}-cfg.py'
    ]
    return create_config(args, env_prefix='{{ cookiecutter.package_name.upper() }}', defaults=defaults)
