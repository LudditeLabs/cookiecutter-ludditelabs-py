import sys
import click
import logging
import traceback


def setup_root_logger(ctx):
    """Setup root logger.

    This function adds stream handler to root logger and sets level to DEBUG.
    """
    root = logging.getLogger()

    if not root.handlers:
        h = logging.StreamHandler(sys.stdout)
        h.setLevel(logging.DEBUG)
        h.setFormatter(logging.Formatter('%(message)s'))
        root.addHandler(h)

    logfile = ctx.params['logfile']
    if logfile:
        h = logging.FileHandler(ctx.params['logfile'], 'w')
        h.setFormatter(logging.Formatter('%(message)s'))
        root.addHandler(h)


def setup_app_logger(ctx):
    """Setup global app logger.

    This function adds logger instance to the ``ctx.meta['logger']``.

    Args:
        ctx: Click context.
    """
    setup_root_logger(ctx)

    logger = logging.getLogger('{{ cookiecutter.package_name }}')
    logger.setLevel(logging.DEBUG if ctx.meta.get('verbose') else logging.INFO)
    ctx.meta['logger'] = logger


def get_app_logger():
    """Get application's global logger.

    This function must be called inside Click context.

    Returns:
        Logger instance.
    """
    ctx = click.get_current_context()
    return ctx.meta['logger']


def log_error(logger, exception, prefix=None):
    """Log exception and traceback.

    Args:
        logger: Logger to use.
        exception: Exception to log.
        prefix: String to put before the error.
    """
    lines = traceback.format_exception(type(exception), exception,
                                       exception.__traceback__)
    if prefix:
        lines.insert(0, prefix)
    logger.info(''.join(lines).rstrip())


class LoggerPrefixAdapter(logging.LoggerAdapter):
    """Logger adapter to add prefix to all messages."""

    def __init__(self, logger, prefix, extra=None):
        super(LoggerPrefixAdapter, self).__init__(logger, extra)
        self.prefix = prefix

    def process(self, msg, kwargs):
        if self.extra is not None:
            kwargs['extra'] = self.extra
        msg = ''.join(self.prefix + x for x in msg.splitlines(True))
        return msg, kwargs
