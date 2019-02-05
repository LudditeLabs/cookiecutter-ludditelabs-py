import os.path as op
from config_source import DictConfig


# Define UPPER_CASE attributes.
class AppConfig:
    """Default application's configuration."""

    #: Example config.
    EXAMPLE_CONF = 'hello'


def create_config(*args, env_prefix='{{ cookiecutter.package_name.upper() }}',
                  default_config='~/.{{ cookiecutter.package_name.replace("_", "-") }}-cfg.py'):
    """Create app configuration.

    Configurations precedence:

    * Default configuration from the :class:`AppConfig`.
    * S3 configuration file.
    * Local config files ``config_files``.
    * Environment variables ``<env_prefix>_*``.

    Add the following fields to local config to load S3 config::

        ...

        S3 = dict(
            bucket_name='mybucket',
            filename='path/in/bucket/cfg.py',
            # profile='',
            # access_key='',
            # secret_key='',
            # cache_filename='/path/to/cache/file.py',
            # update_cache=False
        )

    Args:
        args: Configuration filenames to load.
        env_prefix: Environment variables prefix.
        default_config: Default configuration file. It loaded before the
            ``config_files``.

    Returns:
        :class:`DictConfig` instance with loaded configuration.

    Notes:
        It loads only UPPER CASE fields (nested fields may be lower case).

    See Also:
        https://docs.aws.amazon.com/cli/latest/reference/s3/
    """
    config_files = [default_config]
    config_files.extend(args)

    config = DictConfig()
    config.load_from('object', AppConfig)

    for filename in config_files:
        config.load_from('pyfile', op.abspath(op.expanduser(filename)),
                         silent=True)

    config.load_from('env', prefix=env_prefix)

    # If S3 field is set then load S3 config
    # and merge already loaded files/env config into it.
    s3 = config.get('S3')
    if s3 is not None and not s3.get('skip', False):
        s3config = DictConfig(defaults={'s3': s3})
        s3config.load_from('s3')
        s3config.load_from('dict', config)
        config = s3config

    return config
