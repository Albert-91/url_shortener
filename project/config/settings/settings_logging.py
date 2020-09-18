from os.path import join

from .settings_common import *

LOGS_DIR = join(PROJECT_ROOT_DIR, 'logs')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'formatter_logfile': {
            'format': '[{levelname}] {asctime} PID{process:d}T{thread:d} {funcName}@{pathname}:{lineno} - {message}',
            'style': '{',
        },
        'formatter_console': {
            'format': '[{levelname}] {asctime} - {message}',
            'style': '{',
        },
    },

    'filters': {
        'require_debug': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },

    'handlers': {
        'console': {
            # outputs all to console when in DEBUG mode
            'filters': ['require_debug'],
            'class': 'logging.StreamHandler',
            'formatter': 'formatter_console'
        },
        # 'logfile': {
        #     # logs all runtime log messages to file (with logrotate)
        #     'level': 'INFO',
        #     'class': 'logging.handlers.RotatingFileHandler',
        #     'maxBytes': 4 * 1024 ** 2,  # 4MB
        #     'formatter': 'formatter_logfile',
        #     'filename': join(LOGS_DIR, 'url_shortener.log'),
        # },
    },

    'loggers': {
        'project': {
            # 'handlers': ['logfile', 'console'],
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
