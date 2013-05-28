from flask import request, Response, Flask, render_template
import os
import Queue
import re
import requests
import threading
import timeit

app = Flask("pulls")

# Set your github token see https://github.com/blog/1509-personal-api-tokens
github_token = os.environ['ABQ_REVIEW_TOKEN']

# The repos to track
repos = ["https://api.github.com/repos/abiquo/aim",
"https://api.github.com/repos/abiquo/heartbeat",
"https://api.github.com/repos/abiquo/tarantino",
"https://api.github.com/repos/abiquo/commons-amqp",
"https://api.github.com/repos/abiquo/abiquo-chef-agent",
"https://api.github.com/repos/abiquo/abiquo-ucs-client",
"https://api.github.com/repos/abiquo/jclouds-abiquo",
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
"https://api.github.com/repos/abiquo/jclouds-chef",
"https://api.github.com/repos/abiquo/esx-plugin",
"https://api.github.com/repos/abiquo/hyperv-plugin",
"https://api.github.com/repos/abiquo/libvirt-plugin",
"https://api.github.com/repos/abiquo/virtualbox-plugin",
"https://api.github.com/repos/abiquo/xenserver-plugin",
"https://api.github.com/repos/abiquo/oraclevm-plugin",
"https://api.github.com/repos/abiquo/hypervisor-plugin-model",
"https://api.github.com/repos/abiquo/commons-redis",
"https://api.github.com/repos/abiquo/jclouds-labs",
"https://api.github.com/repos/abiquo/nexenta-plugin",
"https://api.github.com/repos/abiquo/netapp-plugin",
"https://api.github.com/repos/abiquo/ec2-plugin",
"https://api.github.com/repos/abiquo/m",
"https://api.github.com/repos/abiquo/commons-test",
"https://api.github.com/repos/abiquo/ui" ]

@app.route("/")
def index():
    summaries = { 'hot' : [] , 'cold' : [] , 'burned' : []}
    threads = []
    results = Queue.Queue()
    start = timeit.default_timer()
    
    for repo_url in repos:
        repo = get(repo_url)
        t = threading.Thread(target=analyze_repo, args=(repo, results,))
        t.start()
        threads.append(t)
    
    [thread.join() for thread in threads]

    while not results.empty():
        summary = results.get()
        summaries[categorize_pull(summary)].append(summary)

    end = timeit.default_timer()
    
    return render_template('index.html', pulls = summaries, process_time = (end-start))

def analyze_repo(repo, results):
    payload = {"state" : "open"}
    pulls = get(repo["pulls_url"].replace("{/number}", ""), payload)
    threads = []

    for pull_head in pulls:
        t = threading.Thread(target=analyze_pull, args=(repo, pull_head, results,))
        t.start()
        threads.append(t)

    [thread.join() for thread in threads]

    return pulls

def analyze_pull(repo, pull_head, results):
    pull = get(pull_head["url"])
    likes, comments = count_comment_likes(pull)
    summary = {}
    summary['name']       = pull["title"]
    summary['url']        = pull["html_url"]
    summary['likes']      = likes
    summary['comments']   = comments
    summary['repo_name']  = repo["name"]
    summary['repo_url']   = repo["html_url"]
    summary['author']     = pull["user"]["login"]
    results.put(summary)

def count_comment_likes(pull):
    comments = get(pull["comments_url"])
    likes = 0
    total_comments = pull["comments"] + pull["review_comments"]
    for comment in comments:
        if re.search("(\+ *1)", comment["body"]):
            likes += 1
    return likes, total_comments

def categorize_pull(pull):
    likes = pull['likes']
    if   likes >= 2 : return 'burned'
    elif likes > 0: return 'hot'
    return 'cold'

def get(url, params = None):
    response = requests.get(url, headers={ "Authorization" :"token " + github_token }, params=params)
    response.raise_for_status()
    json = response.json()
    if "next" in response.links:
        json.extend(get(response.links['next']["url"]))
    return json

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
