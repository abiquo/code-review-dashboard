from auth import requires_auth
from flask import Flask, render_template
from github import Github
import config
import timeit

app = Flask(__name__)


def load_plugin(name):
    module = __import__("plugins." + name, fromlist=["plugins"])
    plugin = module.load()
    plugin_config = plugin.config
    for prop in plugin_config.iterkeys():
        setattr(config, prop, plugin_config[prop])
    return plugin, plugin_config


@app.route("/")
@requires_auth
def index(auth=None):
    plugin, plugin_config = load_plugin(config.PLUGIN)
    github = Github(auth, plugin)

    start = timeit.default_timer()
    result = github.search_pulls()
    end = timeit.default_timer()

    summaries = {'left': [], 'middle': [], 'right': []}
    authors = set()
    branches = set()
    repos = set()
    for pull in result['pulls']:
        summaries[plugin.classify(pull)].append(pull)
        authors.add(pull['author'])
        branches.add(pull['target_branch'])
        repos.add(pull['repo_name'])

    stats = {
        'threads': result['total-threads'],
        'requests': result['total-requests'],
        'rate-limit': result['rate-limit'],
        'process-time': end - start,
        'total-left': len(summaries['left']),
        'total-middle': len(summaries['middle']),
        'total-right': len(summaries['right'])
    }

    return render_template('columns.html',
                           title=plugin_config['title'],
                           headers=plugin_config['headers'],
                           template=plugin_config['template'],
                           stats=stats,
                           pulls=summaries,
                           authors=sorted(authors),
                           branches=sorted(branches),
                           repos=sorted(repos),
                           user=github.user())

if __name__ == "__main__":
    app.debug = True
    app.run(host=config.LISTEN_ADDRESS)
