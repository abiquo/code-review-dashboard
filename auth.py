from flask import session
from functools import wraps


class Token(object):
    def __init__(self, token):
        self.token = token
        self.user = ''
        self.name = ''


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = None
        if 'token' in session:
            temp = session['token']
            auth = Token(temp.get('token', None))
            auth.user = temp.get('user', None)
            auth.name = temp.get('name', None)

        kwargs['auth'] = auth
        return f(*args, **kwargs)
    return decorated
