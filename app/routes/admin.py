from flask import Blueprint, render_template, Response
from flask_login import login_required
from ..decorators import is_admin
from ..util import sse
import time
from extensions import announcer

adminRoutes = Blueprint("admin", __name__, template_folder="../templates")
counter = 11

@adminRoutes.route("/")
@login_required
@is_admin
def home():
    return render_template("admin/index.html", title="Admin dashboard", hasNavbar=True)


@adminRoutes.route("/general-content")
@login_required
@is_admin
def load_general_content():
    return "<h1>Truy vấn về hệ thống - Output CHART</h1>"


@adminRoutes.route("/stats-data")
@login_required
@is_admin
def stats_data():

    def stream():
        messages = announcer.listen()  # returns a queue.Queue
        while True:
            # global counter
            # counter += 1
            msg = messages.get()  # blocks until a new message arrives
            yield msg
            time.sleep(2.0)

    return Response(stream(), mimetype='text/event-stream')

@adminRoutes.route("/manage-users")
@is_admin
def manage_users():

    return render_template("")
