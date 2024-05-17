# gunicorn_config.py

# Host and port to bind to (listen on all interfaces)
bind = '192.168.1.75:5000'

# Number of worker processes (adjust based on server resources)
workers = 13

# Timeout for worker processes (in seconds)
timeout = 60

# Set the maximum requests a worker will process before restarting
max_requests = 1000

# Set the maximum number of requests a worker will handle before graceful restart
max_requests_jitter = 50

# Enable or disable daemon mode
daemon = False

# Set Gunicorn to log errors to stderr
errorlog = '-'

# run using command
# waitress-serve --listen=0.0.0.0:5000 app:app