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
        self.repos = self._abiquo_repos()

    def parse_pull(self, pull, data):
        data['obsolete'] = data['old'] >= 2
        data['likes'] = 0
        data['dislikes'] = 0
        data['canadian'] = False

    def parse_comment(self, comment, data):
        data['canadian'] = self._is_canadian(comment)
        data['agorilado'] = self._is_agorilado(comment)
        if self._has_like(comment):
            data['likes'] = data['likes'] + 1
        if self._has_dislike(comment):
            data['dislikes'] = data['dislikes'] + 1

    def classify(self, pull):
        likes = pull['likes']
        if likes >= 2:
            return 'right'
        elif likes > 0:
            return 'middle'
        return 'left'

    def _is_canadian(self, comment):
        if re.search("Leader Seal of Approval", comment["body"]):
            return True
        return False

    def _is_agorilado(self, comment):
        return comment['user']['login'] == 'apuig'

    def _has_like(self, comment):
        for pattern in ["\+1", ":shoe:\s*:soccer:", ":shipit:"]:
            if re.search(pattern, comment["body"]):
                return True
        return False

    def _has_dislike(self, comment):
        if re.search("\-1", comment["body"]):
            return True
        return False

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
                "https://api.github.com/repos/abiquo/tutorials"]
