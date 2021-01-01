from flask import Blueprint, render_template

lecturer = Blueprint("lecturer", __name__, template_folder="../templates")


@lecturer.route("/")
def lecturer_home():
    return render_template("lecturer/index.html")
