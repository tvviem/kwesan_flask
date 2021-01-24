from flask import Blueprint, render_template

adminRoutes = Blueprint("admin", __name__, template_folder="../templates")


@adminRoutes.route("/")
# @login_required
def home():
    return render_template("admin/index.html", title="Admin dashboard", hasNavbar=True)