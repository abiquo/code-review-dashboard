#################
# Configuration #
#################

LISTEN_ADDRESS = '0.0.0.0'      # Address where the application listens
LISTEN_PORT = 80                # Port where the application listens
PLUGIN = 'abiquo'               # The plugin to load
DEBUG = True                    # Print debut information
THREADED = True                 # Use multiple threads to perform the Github API calls
MAX_RETRIES = 5                 # Number of retries for failed requests
DELAY = 1                       # The default delay (in seconds) to wait before retrying failed requests
BACKOFF = 2                     # The backoff factor to wait between retries
CLIENT_ID = 'CHANGE_ME'         # Github client ID
CLIENT_SECRET = 'CHANGE_ME'     # Github client secret
SECRET_KEY = 'CHANGE_ME'        # Flask app secret key (to decrypt cookies, better shared across all instances)
