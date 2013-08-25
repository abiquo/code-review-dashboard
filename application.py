from auth import requires_auth
from flask import Flask, render_template
from github import Github
import config
import timeit

app = Flask(__name__)


@app.route("/")
@requires_auth
def index(auth=None):
    github = Github(auth)
    user = github.user()

    start = timeit.default_timer()
    result = github.search_pulls()
    end = timeit.default_timer()

    summaries = {'left': [], 'middle': [], 'right': []}
    for pull in result['pulls']:
        summaries[categorize_pull(pull)].append(pull)

    stats = {
        'threads': result['total-threads'],
        'requests': result['total-requests'],
        'rate-limit': result['rate-limit'],
        'process-time': end - start,
        'total-left': len(summaries['left']),
        'total-middle': len(summaries['middle']),
        'total-right': len(summaries['right'])
    }

    view = {
        'title': config.TITLE,
        'headers': config.HEADERS,
        'template': config.TEMPLATE,
    }

    return render_template('columns.html',
                           view=view,
                           stats=stats,
                           pulls=summaries,
                           old_days=config.OLD_DAYS,
                           user=user)


def categorize_pull(pull):
    likes = pull['likes']
    if likes >= 2:
        return 'right'
    elif likes > 0:
        return 'middle'
    return 'left'


if __name__ == "__main__":
    app.debug = True
    app.run(host=config.LISTEN_ADDRESS)
