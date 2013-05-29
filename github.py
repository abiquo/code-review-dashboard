import datetime
import Queue
import re
import requests
import threading


class Github:
    def __init__(self, repos, credentials):
        self.repos = repos
        self.credentials = credentials
        self.total_threads = 0
        self.total_requests = 0
        self.remaining_rl = 5000

    def search_pulls(self):
        threads = []
        results = Queue.Queue()

        for repo_url in self.repos:
            repo = self.get(repo_url)
            t = threading.Thread(target=self._analyze_repo,
                                 args=(repo, results,))
            t.start()
            threads.append(t)

        [thread.join() for thread in threads]
        self.__incr_threads(len(threads))

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
            t = threading.Thread(target=self._analyze_pull,
                                 args=(repo, pull_head, results,))
            t.start()
            threads.append(t)

        [thread.join() for thread in threads]
        self.__incr_threads(len(threads))

        return pulls

    def _analyze_pull(self, repo, pull_head, results):
        pull = self.get(pull_head["url"])
        likes, comments = self._count_comment_likes(pull)
        summary = {}
        summary['name'] = pull["title"]
        summary['url'] = pull["html_url"]
        summary['likes'] = likes
        summary['comments'] = comments
        summary['repo_name'] = repo["name"]
        summary['repo_url'] = repo["html_url"]
        summary['author'] = pull["user"]["login"]
        summary['old'] = self._get_days_old(pull)
        results.put(summary)

    def _count_comment_likes(self, pull):
        comments = self.get(pull["comments_url"])
        likes = 0
        total_comments = pull["comments"] + pull["review_comments"]
        for comment in comments:
            if re.search("(\+ *1)", comment["body"]):
                likes += 1
        return likes, total_comments

    def _get_days_old(self, pull):
        last_updated = pull['updated_at']
        dt = datetime.datetime.strptime(last_updated, '%Y-%m-%dT%H:%M:%SZ')
        today = datetime.datetime.today()
        return (today - dt).days

    def get(self, url, params=None):
        auth = "Basic %s" % self.credentials.encoded()
        response = requests.get(url,
                                headers={"Authorization": auth},
                                params=params)

        self.__incr_requests()
        self.__update_rl(response)

        response.raise_for_status()
        json = response.json()
        if "next" in response.links:
            json.extend(self.get(response.links['next']["url"]))
        return json

    def __incr_requests(self):
        rlock = threading.RLock()
        with rlock:
            self.total_requests += 1

    def __update_rl(self, response):
        rlock = threading.RLock()
        with rlock:
            new_rl = int(response.headers['X-RateLimit-Remaining'])
            if new_rl < self.remaining_rl:
                self.remaining_rl = new_rl

    def __incr_threads(self, num_threads):
        rlock = threading.RLock()
        with rlock:
            self.total_threads += num_threads
