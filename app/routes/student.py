from flask import Blueprint, render_template

studentRoutes = Blueprint("student", __name__, template_folder="../templates")


@studentRoutes.route("/")
def student_home():
    return render_template("student/index.html", hasNavbar=True)