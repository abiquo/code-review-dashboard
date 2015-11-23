import os

#################
# Configuration #
#################

# Github authentication variables
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
SECRET_KEY = os.environ.get('SECRET_KEY')

# Web server options
LISTEN_ADDRESS = os.environ.get('LISTEN_ADDRESS') or '0.0.0.0'
LISTEN_PORT = int(os.environ.get('LISTEN_PORT') or 8080)

# Name of the dashboard template to load
DASHBOARD = os.environ.get('DASHBOARD') or 'default'

# Turn on debugging output
DEBUG = os.environ.get('DEBUG') == 'true'

# Inspect pull requests in several threads
THREADED = os.environ.get('THREADED') == 'true'

# Customize HTTP retry policy
MAX_RETRIES = int(os.environ.get('MAX_RETRIES') or 5)
DELAY = int(os.environ.get('DELAY') or 1)
BACKOFF = int(os.environ.get('BACKOFF') or 2)
