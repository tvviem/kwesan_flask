from flask import Blueprint, render_template

loginPage = Blueprint("login", __name__, template_folder="templates")
indexPage = Blueprint("index", __name__, template_folder="templates")


@indexPage.route("/")
@indexPage.route("/index")
def index():
    return render_template("index.html")


@loginPage.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")