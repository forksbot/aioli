# -*- coding: utf-8 -*-

import sys


LOGGING_CONFIG_DEFAULTS = dict(
    version=1,
    disable_existing_loggers=False,
    loggers={
        'root': {
            'level': 'INFO',
            'handlers': ['console']
        },
        'peewee': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': True,
        },
        'pkg': {
            'level': 'INFO',
            'handlers': ['pkg_console'],
            'propagate': True,
        },
        'aiohttp': {
            'level': 'INFO',
            'handlers': ['app_console'],
            'propagate': True,
            'qualname': 'aiohttp.internal',
        },
        'aiohttp.access': {
            'level': 'INFO',
            'handlers': ['access_console'],
            'propagate': True,
            'qualname': 'aiohttp.access',
        },
    },
    handlers={
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'generic',
            'stream': sys.stdout
        },
        'app_console': {
            'class': 'logging.StreamHandler',
            'formatter': 'generic',
            'stream': sys.stdout,
        },
        'access_console': {
            'class': 'logging.StreamHandler',
            'formatter': 'access',
            'stream': sys.stdout,
        },
        'pkg_console': {
            'class': 'logging.StreamHandler',
            'formatter': 'pkg',
            'stream': sys.stdout
        },
    },
    formatters={
        'pkg': {
            'format': '[%(levelname)1.1s %(asctime)s.%(msecs)03d %(name)s] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'class': 'logging.Formatter'
        },
        'access': {
            'format': '[%(levelname)1.1s %(asctime)s.%(msecs)03d %(process)d] '
                      '%(request)s - client: %(host)s, status: %(status)d, size: %(byte)d',
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'class': 'logging.Formatter',
        },
        'generic': {
            'format': '[%(levelname)1.1s %(asctime)s.%(msecs)03d] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'class': 'logging.Formatter'
        },
    }
)
