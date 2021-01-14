from flask import Blueprint, render_template

admin = Blueprint("admin", __name__, template_folder="../templates")


@admin.route("/")
def home():
    return render_template("admin/index.html", title="Admin dashboard", hasNavbar=True)
