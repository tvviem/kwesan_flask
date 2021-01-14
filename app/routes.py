from flask import Blueprint, render_template

# alias user use in template with href="{{ url_for('user.<method_name>') }}"
userPage = Blueprint("user", __name__, template_folder="templates")
indexPage = Blueprint("index", __name__, template_folder="templates")


@indexPage.route("/")
def index():
    return render_template("index.html", hasNavbar=True)


@userPage.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html", hasNavbar=False)


@userPage.route("/register", methods=["GET", "POST"])
def register():
    return render_template("signup.html", hasNavbar=False)