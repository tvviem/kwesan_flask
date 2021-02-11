from flask import Blueprint, render_template
from ..decorators import is_lecturer
from flask_login import login_required

lecturerRoutes = Blueprint("lecturer", __name__, template_folder="../templates")


@lecturerRoutes.route("/")
@login_required
@is_lecturer
def home():
    return render_template("lecturer/index.html", hasNavbar=True)
