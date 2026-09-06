import logging

from flask import Flask

from app.routes.cliente_route import cliente_bp
from database import close_db_session


def create_app():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s [%(levelname)s %(name)s : %(message)s]"
    )

    app = Flask(__name__)

    app.teardown_appcontext(close_db_session)
    app.register_blueprint(cliente_bp)

    return app
