# gunicorn_config.py
import os
import multiprocessing
import logging
import sys
from datetime import datetime

# Bind to 0.0.0.0:8000
bind = "0.0.0.0:8000"

# Number of worker processes
# A good rule of thumb is 2-4 workers per CPU core
workers = int(os.environ.get("GUNICORN_WORKERS", multiprocessing.cpu_count() * 2 + 1))

# Worker class to use
worker_class = "sync"

# The maximum number of requests a worker will process before restarting
max_requests = 100
max_requests_jitter = 0

threads = 10

# Timeout (in seconds) for a request to be processed
timeout = 30

# Log level
loglevel = "info"

# Custom formatter that properly shows milliseconds
class MillisecondFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        ct = datetime.fromtimestamp(record.created)
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            t = ct.strftime("%Y-%m-%d %H:%M:%S")
            s = "%s.%03d" % (t, int(record.msecs))
        return s

# Logging configuration
logconfig_dict = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            '()': MillisecondFormatter,
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S.%03d'
        },
        'access': {
            '()': MillisecondFormatter,
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S.%03d'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'stream': sys.stdout
        },
        'error_console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'stream': sys.stderr
        },
        'access_console': {
            'class': 'logging.StreamHandler',
            'formatter': 'access',
            'stream': sys.stdout
        }
    },
    'loggers': {
        'gunicorn.error': {
            'handlers': ['error_console'],
            'level': 'INFO',
            'propagate': False
        },
        # 'gunicorn.access': {
        #     'handlers': ['access_console'],
        #     'level': 'INFO',
        #     'propagate': False
        # }
    }
}

# Custom access log format including millisecond timestamps
accesslog = "false"  # Log to stdout
errorlog = "-"  # Log to stdout
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(L)s'