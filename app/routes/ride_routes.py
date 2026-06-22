from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for

from app.auth import current_user, login_required
from use_cases.exceptions import ValidationError

bp = Blueprint("rides", __name__)


@bp.route("/caronas", methods=["GET"])
@login_required
def index():
    user = current_user()
    search = request.args.get("busca", "")
    rides = current_app.container.list_available_rides.execute(user.id, search)
    return render_template("rides/index.html", rides=rides, search=search)


@bp.route("/caronas/nova", methods=["GET"])
@login_required
def create():
    old = session.pop("old", {})
    return render_template("rides/create.html", old=old)


@bp.route("/caronas", methods=["POST"])
@login_required
def store():
    user = current_user()
    try:
        current_app.container.offer_ride.execute(
            user.id,
            {
                "origin": request.form.get("origin"),
                "destination": request.form.get("destination"),
                "departure_at": request.form.get("departure_at"),
                "seats_total": request.form.get("seats_total"),
                "price_per_seat": request.form.get("price_per_seat"),
            },
        )
        flash("Carona publicada com sucesso!", "success")
        return redirect(url_for("rides.index"))
    except ValidationError as e:
        flash(e.as_text(), "error")
        session["old"] = request.form.to_dict()
        return redirect(url_for("rides.create"))

