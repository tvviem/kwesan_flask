from flask import abort, make_response, current_app as app, request, redirect, url_for, g
from flask_login import current_user
from functools import wraps


def is_admin(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin():
            abort(403)
        return func(*args, **kwargs)

    return decorated_function


def is_lecturer(func):
    def wrapper():
        if not current_user.is_lecturer():
            abort(403)
        func()

    return wrapper