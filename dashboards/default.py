import datetime
import re


def load():
    """ Loads the base dashboard. """
    return BaseDashboard()


class BaseDashboard:
    """ Customizes the review dashboard and provides
        custom pull request and comment parsers. """

    def __init__(self):
        """ Configure the view and the repos to be scanned """
        self.config = {
            'title': 'Code Review Dashboard',
            'headers': { 'left': 'Need More Work',
                         'middle': 'Build Passing',
                         'right': 'Someone Likes!' },
            'template': 'default.html',
        }

    def parse_pull(self, pull, data):
        """ Parse the pull request object and populate any additional
            data that is going to be accessed when rendering the dashboard. """
        data['obsolete'] = data['old'] >= 180
        data['likes'] = 0
        data['dislikes'] = 0

    def parse_comment(self, comment, data):
        """ Parse the comment object and populate any additional
            data that is going to be accessed when rendering the dashboard. """
        created = datetime.datetime.strptime(comment['created_at'],
                                             '%Y-%m-%dT%H:%M:%SZ')
        if self._has(comment, ['\+1', 'lgtm', 'LGTM', ':shipit:']):
            data['likes'] = data['likes'] + 1
        elif self._has(comment, ['\-1']):
            data['dislikes'] = data['dislikes'] + 1

    def classify(self, pull):
        """ Invoked once the pull request has been completely parsed.
            This method returns the column where the pull request must appear. """
        likes = pull['likes']
        dislikes = pull['dislikes']

        if dislikes > 0:
            return 'left'
        if likes > 0:
            return 'right'
        elif pull['build_status'] == 'success':
            return 'middle'
        elif pull['build_status'] == 'failure':
            return 'left'
        else:
            return 'left'

    def _has(self, comment, patterns):
        for pattern in patterns:
            if re.search(pattern, comment["body"]):
                return True
        return False
