########################
# Global configuration #
########################

LISTEN_ADDRESS = '0.0.0.0'                  # Address where the application listens
TITLE = 'Abiquo Code Review Dashboard'      # The title to display
HEADERS = { 'left': 'Cold',                 # The title for each columns
            'middle': 'Hot!',
            'right': 'Burning'}
TEMPLATE = 'basic.html'                     # The template to render
OLD_DAYS = 2                                # Number of days to consider a pull request 'old'
OK_PATTERNS = ["\+1", ":shoe:\s*:soccer:"]  # The patterns that are considered an OK

#####################
# I/O configuration #
#####################

DEBUG = True        # Print debut information
THREADED = True     # Use multiple threads to perform the Github API calls
MAX_RETRIES = 5     # Number of retries for failed requests
DELAY = 1           # The default delay (in seconds) to wait before retrying failed requests
BACKOFF = 2         # The backoff factor to wait between retries

#######################
# Watch configuration #
#######################

# The repos to track
# ORG = 'abiquo'   # Use this to watch all repos of the organization
# USER = 'nacx'    # Use this to watch all repos of the user
# REPOS = [<repo api-url list>]       # Use this to watch a fixed repo list
ORG = None
USER = None
REPOS = ["https://api.github.com/repos/abiquo/aim",
         "https://api.github.com/repos/abiquo/heartbeat",
         "https://api.github.com/repos/abiquo/tarantino",
         "https://api.github.com/repos/abiquo/commons-amqp",
         "https://api.github.com/repos/abiquo/abiquo-chef-agent",
         "https://api.github.com/repos/abiquo/abiquo-ucs-client",
         "https://api.github.com/repos/abiquo/clientui",
         "https://api.github.com/repos/abiquo/system-properties",
         "https://api.github.com/repos/abiquo/appliance-manager",
         "https://api.github.com/repos/abiquo/aim-client-java",
         "https://api.github.com/repos/abiquo/storage-manager",
         "https://api.github.com/repos/abiquo/conversion-manager",
         "https://api.github.com/repos/abiquo/monitor-manager",
         "https://api.github.com/repos/abiquo/discovery-manager",
         "https://api.github.com/repos/abiquo/api",
         "https://api.github.com/repos/abiquo/model",
         "https://api.github.com/repos/abiquo/storage-plugin-lvm",
         "https://api.github.com/repos/abiquo/flex-client-stub",
         "https://api.github.com/repos/abiquo/commons-webapps",
         "https://api.github.com/repos/abiquo/maven-archetypes",
         "https://api.github.com/repos/abiquo/task-service",
         "https://api.github.com/repos/abiquo/jclouds",
         "https://api.github.com/repos/abiquo/jclouds-labs",
         "https://api.github.com/repos/abiquo/jclouds-chef",
         "https://api.github.com/repos/abiquo/esx-plugin",
         "https://api.github.com/repos/abiquo/hyperv-plugin",
         "https://api.github.com/repos/abiquo/libvirt-plugin",
         "https://api.github.com/repos/abiquo/virtualbox-plugin",
         "https://api.github.com/repos/abiquo/xenserver-plugin",
         "https://api.github.com/repos/abiquo/oraclevm-plugin",
         "https://api.github.com/repos/abiquo/hypervisor-plugin-model",
         "https://api.github.com/repos/abiquo/commons-redis",
         "https://api.github.com/repos/abiquo/nexenta-plugin",
         "https://api.github.com/repos/abiquo/netapp-plugin",
         "https://api.github.com/repos/abiquo/ec2-plugin",
         "https://api.github.com/repos/abiquo/m",
         "https://api.github.com/repos/abiquo/commons-test",
         "https://api.github.com/repos/abiquo/ui",
         "https://api.github.com/repos/abiquo/code-review-dashboard",
         "https://api.github.com/repos/abiquo/platform"]
