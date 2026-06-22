from functools import wraps
from typing import Optional

from flask import current_app, g, redirect, session, url_for

from domain.user import User


def current_user() -> Optional[User]:
    """Usuário autenticado na sessão atual, com cache por requisição em `g`."""
    if "user" in g:
        return g.user

    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
        return None

    g.user = current_app.container.users.find_by_id(int(user_id))
    return g.user


def login_user(user: User) -> None:
    session["user_id"] = user.id
    g.user = user


def logout_user() -> None:
    session.pop("user_id", None)
    g.user = None


def login_required(view_func):
    """Garante que há usuário autenticado antes de executar a rota; caso
    contrário, redireciona ao login com uma mensagem flash.
    """

    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if current_user() is None:
            return redirect(url_for("auth.show_register"))
        return view_func(*args, **kwargs)

    return wrapped
