"""Logging configuration is here"""


def configure_logging():
    import logging.config
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(levelname)s:%(name)s: %(message)s '
                          '(%(asctime)s; %(filename)s:%(lineno)d)',
                'datefmt': "%Y-%m-%d %H:%M:%S",
            }
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            '': {
                'handlers': ['console'],
                'level': 'DEBUG',
            },
        }
    }
    logging.config.dictConfig(LOGGING)
