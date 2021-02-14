from flask import Blueprint, render_template
from flask_login import login_required
from ..decorators import is_admin

adminRoutes = Blueprint("admin", __name__, template_folder="../templates")


@adminRoutes.route("/")
@login_required
@is_admin
def home():
    return render_template("admin/index.html", title="Admin dashboard", hasNavbar=True)


@adminRoutes.route("/general-content")
@login_required
@is_admin
def load_general_content():
    return "<h1>Truy vấn nội dung tổng quát về hệ thống</h1>"