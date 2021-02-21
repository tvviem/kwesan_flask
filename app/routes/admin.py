from flask import Blueprint, render_template, Response, jsonify
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
    template_rendered = render_template("admin/mainshow.html")
    # print(template_rendered)
    response_object = {
          "status": "success",
          "message": "success",
          "data": {"content": template_rendered}
    }
    return jsonify(response_object)
    # return "<div id='content'><h1>Truy vấn về hệ thống - Output CHART</h1></div>"


@adminRoutes.route("/manage-users")
@is_admin
def manage_users():
    template_rendered = render_template("admin/manage_users.html")

    response_object = {
          "status": "success",
          "data": {"content": template_rendered}
    }
    return jsonify(response_object)

    # return Response(render_template("admin/manage_users.html", mimetype='text/html'))

@adminRoutes.route("/manage-questions")
@is_admin
def manage_questions():

    return  render_template("admin/manage_users.html")


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