import re

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for

from app.auth import current_user, login_required, login_user
from app.constants import BRAZILIAN_DDDS

bp = Blueprint("profile", __name__)


def _split_phone(stored: str) -> tuple[str, str]:
    """Separa o telefone armazenado (DDD + número, só dígitos) em DDD e
    número formatado para preencher o formulário de edição."""
    digits = re.sub(r"\D", "", stored or "")
    if digits == "":
        return "", ""

    ddd, rest = digits[:2], digits[2:]
    if len(rest) == 8:
        phone = f"{rest[:4]}-{rest[4:]}"
    elif len(rest) == 9:
        phone = f"{rest[:5]}-{rest[5:]}"
    else:
        phone = rest
    return ddd, phone


@bp.route("/perfil", methods=["GET"])
@login_required
def edit():
    user = current_user()
    ddd, phone = _split_phone(user.phone or "")
    return render_template("profile/edit.html", user=user, ddd=ddd, phone=phone, ddds=BRAZILIAN_DDDS)


@bp.route("/perfil/atualizar", methods=["POST"])
@login_required
def update():
    user = current_user()
    updated = current_app.container.update_profile.execute(
        user,
        request.form.get("name", user.name),
        request.form.get("course", user.course or ""),
        request.form.get("ddd", ""),
        request.form.get("phone", user.phone or ""),
    )
    login_user(updated)
    flash("Perfil atualizado com sucesso!", "success")
    return redirect(url_for("profile.edit"))
