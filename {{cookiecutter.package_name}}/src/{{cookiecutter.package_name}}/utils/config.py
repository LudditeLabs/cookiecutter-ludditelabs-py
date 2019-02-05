from config_source import DictConfig, DictConfigLoader


def create_config(source, env_prefix=None, defaults=None):
    """Create app configuration.

    Configurations precedence:

    * ``defaults``.
    * S3 configuration file.
    * ``source``.
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
        source: Single configuration source or list of them (filenames,
            dictionaries or objects or classes).
        env_prefix: Environment variables prefix.
        defaults: Single configuration source or list of them with
            default configurations. Loaded before the ``source``.

    Returns:
        :class:`DictConfig` instance with loaded configuration.

    Notes:
        It loads only UPPER CASE fields (nested fields may be lower case).

    See Also:
        https://docs.aws.amazon.com/cli/latest/reference/s3/
    """
    if isinstance(defaults, (tuple, list)):
        config_sources = defaults[:]
    elif defaults is not None:
        config_sources = [defaults]
    else:
        config_sources = []

    if isinstance(source, (tuple, list)):
        config_sources.extend(source)
    elif source:
        config_sources.append(source)

    config = DictConfig(defaults={'pyfile': {'silent': True}})
    loader = DictConfigLoader(config)

    for src in config_sources:
        loader.load(src)

    if env_prefix is not None:
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
