# -*- coding: utf-8 -*-

import sys

LOGGING_CONFIG_DEFAULTS = dict(
    version=1,
    disable_existing_loggers=False,
    loggers={
        'root': {
            'level': 'DEBUG',
            'handlers': ['pkg_console'],
            'propagate': False,
        },
        'databases': {
            'level': 'DEBUG',
            'handlers': ['pkg_console'],
            'propagate': False,
        },
        'sqlalchemy': {
            'level': 'DEBUG',
            'handlers': ['pkg_console'],
            'propagate': False,
        },
        'aioli': {
            'level': 'DEBUG',
            'handlers': ['pkg_console'],
            'propagate': False,
        },
        'uvicorn': {
            'level': 'DEBUG',
            'handlers': ['pkg_console'],
            'propagate': False,
        },
    },
    handlers={
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'generic',
            'stream': sys.stdout
        },
        'request_console': {
            'class': 'logging.StreamHandler',
            'formatter': 'access',
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
            'format': '[%(levelname)1.1s %(asctime)s.%(msecs)03d %(process)d] %(message)s',
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
