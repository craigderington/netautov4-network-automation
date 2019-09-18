from datetime import datetime, timedelta
from flask import Blueprint, jsonify, url_for, render_template, request, Response
from netauto import db
from netauto.models import User, Message, Alerts, Locations
from netauto.tasks import log, long_task, get_locations

# home blueprint
home = Blueprint("home", __name__, template_folder="templates")


@home.before_app_first_request
def init_db():
    db.create_all()
    db.session.commit()


@home.route("/", methods=["GET"])
@home.route("/index", methods=["GET", "POST"])
def index():
    return render_template(
        "index.html",
        today=get_date()
    )

@home.route("/longtask", methods=["POST"])
def longtask():
    task = long_task.apply_async()
    return jsonify({"task": task.id}), 202, {"Location": url_for("home.taskstatus",
                                                  task_id=task.id)}


@home.route("/status/<task_id>", methods=["GET", "POST"])
def taskstatus(task_id):
    task = long_task.AsyncResult(task_id)
    if task.state == "PENDING":
        # job did not start yet
        response = {
            "state": task.state,
            "status": "Pending..."
        }
    elif task.state != "FAILURE":
        response = {
            "state": task.state,
            "current": task.info.get("current", 0),
            "total": task.info.get("total", 1),
            "status": task.info.get("status", "")
        }
        if "result" in task.info:
            response["result"] = task.info["result"]
    else:
        # something went wrong in the background job
        response = {
            "state": task.state,
            "current": 1,
            "total": 1,
            "status": str(task.info),  # this is the exception raised
        }
    
    return jsonify(response)


@home.route("/alerts")
def alerts():
    alerts = Alerts.query.all()
    return render_template(
        "index.html",
        alerts=alerts
    )


def get_date():
    """
    Return date as string
    """
    return datetime.now().strftime("%c")
