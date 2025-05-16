# gunicorn_config.py
import os
import multiprocessing
import logging
import sys
from datetime import datetime

# Network binding
bind = os.environ.get("GUNICORN_BIND", "0.0.0.0:8000")

# Number of worker processes
# A good rule of thumb is 2-4 workers per CPU core
workers = int(os.environ.get("GUNICORN_WORKERS", multiprocessing.cpu_count() * 2 + 1))

# Worker class to use
worker_class = "uvicorn.workers.UvicornWorker"

# The maximum number of requests a worker will process before restarting
# Helps prevent memory leaks by recycling workers. 0 -> no restarts
max_requests = int(os.environ.get("GUNICORN_MAX_REQUESTS", "0"))

# Add jitter to max_requests to avoid all workers restarting at once
max_requests_jitter = int(os.environ.get("GUNICORN_MAX_REQUESTS_JITTER", "10"))

# Enable SO_REUSEPORT for better performance (Linux 3.9+)
reuse_port = os.environ.get("GUNICORN_REUSE_PORT", "True").lower() == "true"

# Pre-load application code before forking worker processes
preload_app = os.environ.get("GUNICORN_PRELOAD_APP", "True").lower() == "true"

# Number of threads per worker
threads = int(os.environ.get("GUNICORN_THREADS", "10"))

# Timeout (in seconds) for a request to be processed
timeout = int(os.environ.get("GUNICORN_TIMEOUT", "30"))

################### Logging

# Log level
loglevel = os.environ.get("GUNICORN_LOG_LEVEL", "info")

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
        },
        'access': {
            '()': MillisecondFormatter,
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
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
