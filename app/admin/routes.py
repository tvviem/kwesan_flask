from flask import Blueprint, render_template

admin = Blueprint("admin", __name__, template_folder="../templates")


@admin.route("/")
def admin_home():
    return render_template("base.html")
