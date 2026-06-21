import hmac
import secrets

from flask import abort, request, session


def csrf_token() -> str:
    """Gera (uma vez por sessão) e devolve o token CSRF embutido nos forms."""
    token = session.get("_csrf")
    if not token:
        token = secrets.token_hex(32)
        session["_csrf"] = token
    return token


def validate_csrf_or_abort() -> None:
    """Toda requisição que altera estado (POST) precisa do token CSRF válido."""
    if request.method != "POST":
        return

    sent = request.form.get("_token", "")
    expected = session.get("_csrf", "")
    if not expected or not hmac.compare_digest(expected, sent):
        abort(400, description="Sessão expirada. Volte à página anterior e tente novamente.")
