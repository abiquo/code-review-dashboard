from auth import requires_auth
from flask import Flask, render_template, request, url_for, redirect, session
from github import Github
from auth import Token
import config
import timeit
import requests
import string
import random


app = Flask(__name__)
app.secret_key = config.SECRET_KEY


def load_dashboard(name):
    module = __import__("dashboards." + name, fromlist=["dashboards"])
    dashboard = module.load()
    dashboard_config = dashboard.config
    for prop in dashboard_config.iterkeys():
        setattr(config, prop, dashboard_config[prop])
    return dashboard, dashboard_config


@app.route("/signin")
@requires_auth
def signin(auth=None):
    if not auth:
        return render_template('signin.html')
    else:
        return redirect(url_for('index'))


@app.route('/login')
def authenticate():
    """ According to specification the 'state' must be unpredictable """
    scope = request.args.get('scope')
    if scope:
        scope = 'repo'

    oauth_state = ''.join(random.choice(string.ascii_uppercase +
                                        string.digits) for x in range(32))
    client_id = config.CLIENT_ID
    uri = 'https://github.com/login/oauth/authorize?client_id=' +\
        client_id + '&state=' + oauth_state
    if scope:
        uri = uri + '&scope=' + scope
    return redirect(uri)


@app.route("/authorize")
def authorize():
    try:
        if request.args:
            code = request.args.get('code')
            token = __request_token(code)
            if token:
                session['token'] = {'token': token.token}

    except Exception, e:
        print "Error ", e

    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    if 'token' in session:
        session.pop('token')
    return redirect(url_for('index'))


@app.route("/user/<user>")
@requires_auth
def user(user, auth=None):
    if not auth:
        return redirect(url_for('signin'))
    dashboard, dashboard_config = load_dashboard(config.DASHBOARD)
    github = Github(auth, dashboard)
    dashboard.repos = github.load_user_repos(user)
    return _render_dashboard(dashboard, github)


@app.route("/org/<org>")
@requires_auth
def org(org, auth=None):
    if not auth:
        return redirect(url_for('signin'))
    dashboard, dashboard_config = load_dashboard(config.DASHBOARD)
    github = Github(auth, dashboard)
    dashboard.repos = github.load_org_repos(org)
    return _render_dashboard(dashboard, github)


@app.route("/")
@requires_auth
def index(auth=None):
    if not auth:
        return redirect(url_for('signin'))
    dashboard, dashboard_config = load_dashboard(config.DASHBOARD)
    github = Github(auth, dashboard)
    if not dashboard.repos:
        dashboard.repos = github.load_user_repos(github.user())
    return _render_dashboard(dashboard, github)


def _render_dashboard(dashboard, github):
    start = timeit.default_timer()
    result = github.search_pulls()
    end = timeit.default_timer()

    summaries = {'left': [], 'middle': [], 'right': []}
    authors = set()
    branches = set()
    repos = set()
    for pull in result['pulls']:
        summaries[dashboard.classify(pull)].append(pull)
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
                           title=dashboard_config['title'],
                           headers=dashboard_config['headers'],
                           template=dashboard_config['template'],
                           stats=stats,
                           pulls=summaries,
                           authors=sorted(authors),
                           branches=sorted(branches),
                           repos=sorted(repos),
                           user=github.user())


def __request_token(code):

    client_id = config.CLIENT_ID
    client_secret = config.CLIENT_SECRET
    uri = 'https://github.com/login/oauth/access_token?client_id=' +\
        client_id + '&client_secret=' + client_secret + '&code=' + code

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
