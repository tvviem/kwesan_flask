from flask import Blueprint, render_template

studentPage = Blueprint("student", __name__, template_folder="../templates")


@studentPage.route("/")
def student_home():
    return render_template("student/index.html")