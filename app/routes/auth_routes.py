from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for

from app.auth import current_user, login_user, logout_user
from app.constants import BRAZILIAN_DDDS
from use_cases.exceptions import ValidationError

bp = Blueprint("auth", __name__)


@bp.route("/registrar", methods=["GET"])
def show_register():
    if current_user() is not None:
        return redirect(url_for("rides.index"))
    old = session.pop("old", {})
    return render_template("auth/register.html", old=old, ddds=BRAZILIAN_DDDS)


@bp.route("/registrar", methods=["POST"])
def register():
    try:
        user = current_app.container.register_user.execute(
            request.form.get("name", ""),
            request.form.get("email", ""),
            request.form.get("password", ""),
            request.form.get("course", ""),
            request.form.get("ddd", ""),
            request.form.get("phone", ""),
        )
        login_user(user)
        flash("Conta criada com sucesso. Bem-vindo(a) às caronas!", "success")
        return redirect(url_for("rides.index"))
    except ValidationError as e:
        flash(e.as_text(), "error")
        session["old"] = {
            "name": request.form.get("name", ""),
            "email": request.form.get("email", ""),
            "course": request.form.get("course", ""),
        }
        return redirect(url_for("auth.show_register"))


@bp.route("/logout", methods=["POST"])
def logout():
    logout_user()
    return redirect(url_for("auth.show_register"))
