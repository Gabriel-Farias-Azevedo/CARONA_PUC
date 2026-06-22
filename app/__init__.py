import os
from typing import Optional

from flask import Flask

from app.auth import current_user
from app.container import Container
from app.csrf import csrf_token, validate_csrf_or_abort
from app.routes.auth_routes import bp as auth_bp
from app.routes.home_routes import bp as home_bp
from app.routes.reservation_routes import bp as reservation_bp
from app.routes.ride_routes import bp as ride_bp
from app.template_filters import (format_currency_brl, format_datetime_br,
                                  only_digits)
from infra.db.database import get_connection, init_db


def create_app(db_path: Optional[str] = None) -> Flask:
    """Fábrica de aplicação + raiz de composição: monta a conexão SQLite, liga
    as interfaces de repositório às implementações concretas (Container) e
    registra rotas, filtros de template e proteção CSRF.
    """
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-change-me")

    if db_path is None:
        db_path = os.path.join(app.root_path, "..", "storage", "caronas.sqlite")

    conn = get_connection(db_path)
    init_db(conn)
    app.container = Container.build(conn)

    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(ride_bp)
    app.register_blueprint(reservation_bp)

    app.jinja_env.filters["fmt_dt"] = format_datetime_br
    app.jinja_env.filters["brl"] = format_currency_brl
    app.jinja_env.filters["digits"] = only_digits

    @app.context_processor
    def inject_globals():
        return {"current_user": current_user(), "csrf_token": csrf_token}

    @app.before_request
    def check_csrf():
        validate_csrf_or_abort()

    @app.errorhandler(400)
    def handle_bad_request(error):
        return error.description or "Requisição inválida.", 400

    return app
