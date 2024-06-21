# gunicorn_config.py

import os

# Host and port to bind to (listen on all interfaces)
bind = f"{os.getenv('GUNICORN_BIND_HOST')}:{os.getenv('GUNICORN_BIND_PORT')}"

# Number of worker processes (adjust based on server resources)
workers = int(os.getenv('GUNICORN_WORKERS', 1))

# Timeout for worker processes (in seconds)
timeout = int(os.getenv('GUNICORN_TIMEOUT', 30))

# Set the maximum requests a worker will process before restarting
max_requests = int(os.getenv('GUNICORN_MAX_REQUESTS', 1000))

# Set the maximum number of requests a worker will handle before graceful restart
max_requests_jitter = int(os.getenv('GUNICORN_MAX_REQUESTS_JITTER', 50))

# Enable or disable daemon mode
daemon = os.getenv('GUNICORN_DAEMON', 'false').lower() in ['true', '1', 'yes']

# Set Gunicorn to log errors to stderr
errorlog = '-'
