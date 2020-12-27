from flask import Blueprint

api = Blueprint("api", __name__)


@api.route("/")
def api_home():
    return "<h1>API Home</h1>"


""" Add as many relevant routes as needed. Just like you'd do with an app object. """