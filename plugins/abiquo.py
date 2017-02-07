import re


def load():
    return Abiquo()


class Abiquo:
    def __init__(self):
        self.config = {
            'title': 'Abiquo Code Review Dashboard',
            'headers': {'left': 'Cold', 'middle': 'Hot!', 'right': 'Burning'},
            'template': 'abiquo.html',
        }
        self.authors = {
            'danielestevez': {'unicode': '128169', 'color': '#7E3817', 'title': 'Lidl Commented'},
            'apuig': {'unicode': '128092', 'color': '#7E3817', 'title': 'Agorilado Commented'},
            'enricruiz': {'unicode': '128110', 'color': '#133B78', 'title': 'Thief Commented'},
            'sergicastro': {'unicode': '9891', 'color': '#C45AEC', 'title': 'Sergi Commented with Love'},
            'luciaems': {'unicode': '127814', 'color': '#571B7E', 'title': 'Lucia Commented'},
            'nacx': {'unicode': '128158', 'color': '#FF00DD', 'title': 'Gayer Commented'},
            'aprete': {'unicode': '127829', 'color': '#CC6600', 'title': 'Rumana Commented'}
        }
        self.repos = self._abiquo_repos()

    def parse_pull(self, pull, data):
        data['obsolete'] = data['old'] >= 2
        data['icons'] = []

    def parse_comment(self, comment, data):
        user = comment['user']['login']
        if user in self.authors and not self.authors[user] in data['icons']:
            data['icons'].append(self.authors[user])

    def classify(self, pull):
        likes = pull['likes']
        if likes >= 2:
            return 'right'
        elif likes > 0:
            return 'middle'
        return 'left'

    def _abiquo_repos(self):
        return ["https://api.github.com/repos/abiquo/aim",
                "https://api.github.com/repos/abiquo/tarantino",
                "https://api.github.com/repos/abiquo/commons-amqp",
                "https://api.github.com/repos/abiquo/abiquo-chef-agent",
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
                "https://api.github.com/repos/abiquo/commons-webapps",
                "https://api.github.com/repos/abiquo/task-service",
                "https://api.github.com/repos/abiquo/esx-plugin",
                "https://api.github.com/repos/abiquo/hyperv-plugin",
                "https://api.github.com/repos/abiquo/libvirt-plugin",
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
                "https://api.github.com/repos/abiquo/cloud-provider-proxy",
                "https://api.github.com/repos/abiquo/nfs-plugin",
                "https://api.github.com/repos/abiquo/jclouds-plugin",
                "https://api.github.com/repos/abiquo/platform",
                "https://api.github.com/repos/abiquo/kairosdb-java-client",
                "https://api.github.com/repos/abiquo/azure-plugin",
                "https://api.github.com/repos/abiquo/api-java-client",
                "https://api.github.com/repos/abiquo/abiquo-cookbook",
                "https://api.github.com/repos/abiquo/ui-tests",
                "https://api.github.com/repos/abiquo/docker-plugin",
                "https://api.github.com/repos/abiquo/abiquo-reports",
                "https://api.github.com/repos/abiquo/collectd-abiquo",
                "https://api.github.com/repos/abiquo/collectd-abiquo-cookbook",
                "https://api.github.com/repos/abiquo/watchtower",
                "https://api.github.com/repos/abiquo/jimmy",
                "https://api.github.com/repos/abiquo/nsx-plugin",
                "https://api.github.com/repos/abiquo/vcd-plugin",
                "https://api.github.com/repos/abiquo/avamar-plugin",
                "https://api.github.com/repos/abiquo/veeam-plugin",
                "https://api.github.com/repos/abiquo/tutorials"]
