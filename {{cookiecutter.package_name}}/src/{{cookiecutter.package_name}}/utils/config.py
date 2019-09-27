from config_source import DictConfig, DictConfigLoader


def load_config(sources):
    """Load configuration from the given sources.

    Args:
        sources: Source or list of sources to load.

    Returns:
        :class:`DictConfig` instance.
    """
    config = DictConfig(defaults={'pyfile': {'silent': True}})
    loader = DictConfigLoader(config)

    if isinstance(sources, (tuple, list)):
        config_sources = sources[:]
    elif sources is not None:
        config_sources = [sources]
    else:
        config_sources = []

    for src in config_sources:
        loader.load(src)

    return config


def get_namespace(config, namespace, lowercase=True, trim_namespace=True):
    """Get a subset of options with the given namespace (prefix).

    Args:
        config: Dict-like object with options.
        namespace: Configuration namespace.
        lowercase: Make result options' keys lowercase.
        trim_namespace: Remove namespace prefix from keys.

    Returns:
        Dictionary with options.
    """
    rv = {}
    for k, v in config.items():
        if not k.startswith(namespace):
            continue
        if trim_namespace:
            key = k[len(namespace):]
        else:
            key = k
        if lowercase:
            key = key.lower()
        rv[key] = v
    return rv


def create_config(source, env_prefix=None, defaults=None):
    """Create app configuration.

    Configurations precedence:

    * ``defaults``.
    * S3 configuration file.
    * ``source``.
    * Environment variables ``<env_prefix>_*``.

    Add the following fields to local config to load S3 config::

        S3CONFIG_BUCKET_NAME = 'mybucket'
        S3CONFIG_FILENAME = 'path/in/bucket/cfg.py'
        S3CONFIG_CACHE_FILENAME = '/path/to/cache/file.py'
        S3CONFIG_UPDATE_CACHE = False

        # Skip S3 config loading.
        # S3CONFIG_SKIP = True

        # AWS credentials.
        #
        # NOTE: you may use standard env vars to specify credentials:
        # AWS_PROFILE, AWS_REGION, AWS_DEFAULT_REGION, AWS_ACCESS_KEY,
        # AWS_SECRET_KEY.
        #
        # S3CONFIG_PROFILE = ''
        # S3CONFIG_ACCESS_KEY = ''
        # S3CONFIG_SECRET_KEY = ''

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
    env_config = DictConfig()
    if env_prefix:
        env_config.load_from('env', prefix=env_prefix)

    configs = [
        load_config(defaults),
        load_config(source),
        env_config
    ]

    s3_config = {}
    for config in configs:
        s3 = get_namespace(config, 'S3CONFIG_', lowercase=True)
        if s3:
            s3_config.update(s3)

    # If S3 config exists then load it and put after default.
    if s3_config and not s3_config.get('skip', False):
        s3config = DictConfig(defaults={'s3': s3_config})
        s3config.load_from('s3')
        configs.insert(1, s3config)

    # Merge loaded configs.
    config = {}
    for cfg in configs:
        config.update(cfg)

    return config
