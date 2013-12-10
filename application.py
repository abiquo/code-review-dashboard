from auth import requires_auth
from flask import Flask, render_template, request, url_for, redirect, session
from github import Github
from auth import Token
import config
import timeit
import os
import requests
import string
import random

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY') or config.SECRET_KEY


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
    if not auth:
        return app.send_static_file('html/github-btn.html')

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

    session['token'] = {'token': github.credentials.token,
                        'user': github.credentials.user,
                        'name': github.credentials.name}

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


@app.route('/login')
def authenticate():
    """ According to specification the 'state' must be unpredictable """
    oauth_state = ''.join(random.choice(string.ascii_uppercase +
                                        string.digits) for x in range(32))
    client_id = os.environ.get('CLIENT_ID') or config.CLIENT_ID
    uri = 'https://github.com/login/oauth/authorize?client_id=' +\
        client_id + '&scope=repo&state=' + oauth_state
    return redirect(uri)


@app.route("/authorize")
def authorize():
    try:
        if request.args:
            code = request.args.get('code')
            token = __request_token(code)
            if token:
                session['token'] = {'token': token.token}
                return redirect(url_for('index'), code=302)
    except Exception, e:
        print "Error ", e

    return redirect(url_for('index'), code=302)


@app.route('/logout')
def logout():
    if 'token' in session:
        session.pop('token')
    return redirect(url_for('authorize'))


def __request_token(code):

    client_id = os.environ.get('CLIENT_ID') or config.CLIENT_ID
    client_secret = os.environ.get('CLIENT_SECRET') or config.CLIENT_SECRET
    uri = 'https://github.com/login/oauth/access_token?client_id=' +\
        client_id + '&client_secret=' + client_secret + '&code=' + code +\
        '&redirect_uri=http://dashboardtemp.herokuapp.com/authorize'
    header = {'Content-type:': 'application/json'}
    r = requests.post(uri,
                      headers=header)
    d = dict(s.split('=') for s in r.content.split('&'))
    if 'error' in d:
        return None

    if 'access_token' in d:
        return Token(d['access_token'])

    return Token('')


if __name__ == "__main__":
    app.debug = True
    app.run(host=config.LISTEN_ADDRESS, port=config.LISTEN_PORT)
