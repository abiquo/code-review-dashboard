import base64
from flask import request, Response
from functools import wraps


class BasicAuth:
    def __init__(self, user, password):
        self.user = user
        self.password = password

    def encoded(self):
        return base64.b64encode('%s:%s' % (self.user, self.password))


def authenticate():
    return Response('Unauthorized', 401,
                    {'WWW-Authenticate': 'Basic realm='
                                         '"Enter your Github credentials"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return authenticate()
        kwargs['auth'] = BasicAuth(auth.username, auth.password)
        return f(*args, **kwargs)
    return decorated
