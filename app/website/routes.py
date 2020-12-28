from flask import Blueprint, current_app

website = Blueprint("website", __name__, template_folder="../templates")


@website.route("/")
def website_home():
    return "<h1>Website Home</h1>"