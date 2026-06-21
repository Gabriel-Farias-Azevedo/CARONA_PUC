from flask import Blueprint, current_app, flash, redirect, render_template, url_for

from app.auth import current_user, login_required
from use_cases.exceptions import ValidationError

bp = Blueprint("reservations", __name__)


@bp.route("/caronas/<int:ride_id>/reservar", methods=["POST"])
@login_required
def store(ride_id: int):
    user = current_user()
    try:
        current_app.container.reserve_ride.execute(ride_id, user.id)
        flash("Carona reservada! Combine os detalhes com o motorista.", "success")
    except ValidationError as e:
        flash(e.as_text(), "error")
    return redirect(url_for("reservations.index"))


@bp.route("/reservas", methods=["GET"])
@login_required
def index():
    user = current_user()
    reservations = current_app.container.list_reservations_by_passenger.execute(user.id)
    return render_template("reservations/index.html", reservations=reservations)


@bp.route("/reservas/<int:reservation_id>/cancelar", methods=["POST"])
@login_required
def cancel(reservation_id: int):
    user = current_user()
    try:
        current_app.container.cancel_reservation.execute(reservation_id, user.id)
        flash("Reserva cancelada.", "success")
    except ValidationError as e:
        flash(e.as_text(), "error")
    return redirect(url_for("reservations.index"))
