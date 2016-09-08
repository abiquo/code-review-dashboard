import config
import datetime
import Queue
import requests
import threading
import time
import traceback


class Github:
    def __init__(self, credentials, plugin):
        self.credentials = credentials
        self.total_threads = 0
        self.total_requests = 0
        self.remaining_rl = None
        self.plugin = plugin
        self.plugin.github = self

    def user(self):
        if not self.credentials.user:
            self.__request_user()
        return self.credentials.user

    def name(self):
        if not self.credentials.name:
            self.__request_user()
        return self.credentials.name

    def list_org_repos(self, org):
        url = 'https://api.github.com/orgs/%s/repos' % org
        return [repo['url'] for repo in self.get(url)]

    def list_user_repos(self, user):
        url = 'https://api.github.com/users/%s/repos' % user
        return [repo['url'] for repo in self.get(url)]

    def search_pulls(self):
        threads = []
        results = Queue.Queue()

        for repo_url in self.plugin.repos:
            try:
                repo = self.get(repo_url)
                if config.THREADED:
                    t = threading.Thread(target=self._analyze_repo,
                                         args=(repo, results,))
                    t.start()
                    threads.append(t)
                    for thread in threads:
                        thread.join()
                    self.__incr_threads(len(threads))
                else:
                    self._analyze_repo(repo, results)
            except:
                if config.DEBUG:
                    print "Could not analyze repository: %s" % repo_url
                    traceback.print_exc()

        pulls = []
        while not results.empty():
            pulls.append(results.get())

        return {
            "pulls": pulls,
            "total-threads": self.total_threads,
            "total-requests": self.total_requests,
            "rate-limit": self.remaining_rl
        }

    def _analyze_repo(self, repo, results):
        payload = {"state": "open"}
        pulls = self.get(repo["pulls_url"].replace("{/number}", ""), payload)
        threads = []

        for pull_head in pulls:
            try:
                if config.THREADED:
                    t = threading.Thread(target=self._analyze_pull,
                                         args=(repo, pull_head, results,))
                    t.start()
                    threads.append(t)
                    for thread in threads:
                        thread.join()
                    self.__incr_threads(len(threads))
                else:
                    self._analyze_pull(repo, pull_head, results)
            except:
                if config.DEBUG:
                    print "Could not analyze pull request: %s" % pull_head["url"]

        return pulls

    def _analyze_pull(self, repo, pull_head, results):
        pull = self.get(pull_head["url"])
        summary = {}
        summary['name'] = pull["title"]
        summary['url'] = pull["html_url"]
        summary['repo_name'] = repo["name"]
        summary['repo_url'] = repo["html_url"]
        summary['author'] = pull["user"]["login"]
        summary['old'] = self.get_days_old(pull)
        summary['target_branch'] = pull["base"]["ref"]
        summary['build_status'] = self._get_build_status(pull)

        reactions = self.get_reactions(pull)
        self.plugin.parse_pull(pull, reactions, summary)
        self._analyze_comments(pull, summary)

        results.put(summary)

    def _get_build_status(self, pull):
        statuses = self.get(pull['statuses_url'])
        return statuses[0]['state'] if statuses else "unknown"

    def _analyze_comments(self, pull, summary):
        following = False
        comments = self.get(pull["comments_url"])
        comments.extend(self.get(pull["review_comments_url"]))

        for comment in comments:
            if comment["user"]["login"] == self.user():
                following = True
            self.plugin.parse_comment(comment, summary)

        summary['comments'] = pull["comments"] + pull["review_comments"]
        summary['following'] = following

    def get_days_old(self, pull):
        last_updated = pull['updated_at']
        dt = datetime.datetime.strptime(last_updated, '%Y-%m-%dT%H:%M:%SZ')
        today = datetime.datetime.today()
        return (today - dt).days

    def get_reactions(self, pull):
        reactions = self.get(pull['issue_url'] + '/reactions',
                accept='application/vnd.github.squirrel-girl-preview')
        return map(lambda r: r['content'], reactions)

    def get(self, url, params=None, delay=config.DELAY,
            retries=config.MAX_RETRIES, backoff=config.BACKOFF,
            accept='application/json'):
        if config.DEBUG:
            print "GET %s" % url

        if not params:
            params = {'access_token': self.credentials.token}
        else:
            params['access_token'] = self.credentials.token

        while retries > 1:
            response = requests.get(url, params=params, headers={'Accept': accept})
            self.__incr_requests()
            self.__update_rl(response)

            if response.status_code == requests.codes.ok:
                json = response.json()
                if "next" in response.links:
                    json.extend(self.get(response.links['next']["url"]))
                return json
            elif response.status_code >= 400 and response.status_code < 500:
                response.raise_for_status()
            elif response.status_code >= 500:
                if config.DEBUG:
                    print "Request failed. Retrying in %s seconds" % delay
                time.sleep(delay)
                return self.get(url, params, delay * backoff,
                                retries - 1, backoff)
            else:
                json = response.json()
                if "next" in response.links:
                    json.extend(self.get(response.links['next']["url"]))
                return json

        raise Exception("Request failed after %s retries" % config.MAX_RETRIES)

    def __incr_requests(self):
        rlock = threading.RLock()
        with rlock:
            self.total_requests += 1

    def __update_rl(self, response):
        rate_remaining = response.headers['X-RateLimit-Remaining']
        if rate_remaining is not None:
            new_rl = int(rate_remaining)
            rlock = threading.RLock()
            with rlock:
                if self.remaining_rl is None or new_rl < self.remaining_rl:
                    self.remaining_rl = new_rl

    def __incr_threads(self, num_threads):
        rlock = threading.RLock()
        with rlock:
            self.total_threads += num_threads

    def __request_user(self):
        url = 'https://api.github.com/user'
        r = self.get(url)
        self.credentials.user = r['login']
        self.credentials.name = r['name']
