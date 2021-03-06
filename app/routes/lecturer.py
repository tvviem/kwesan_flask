from flask import Blueprint, render_template

lecturerRoutes = Blueprint("lecturer", __name__, template_folder="../templates")


@lecturerRoutes.route("/")
def lecturer_home():
    return render_template("lecturer/index.html", hasNavbar=True)
