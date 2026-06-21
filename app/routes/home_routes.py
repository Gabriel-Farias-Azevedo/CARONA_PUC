from flask import Blueprint, redirect, render_template, url_for

from app.auth import current_user

bp = Blueprint("home", __name__)


@bp.route("/")
def index():
    if current_user() is not None:
        return redirect(url_for("rides.index"))
    return render_template("home.html")
