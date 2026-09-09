import logging

from flask import Flask

from app.routes.auto_route import auto_blp
from app.routes.cliente_route import cliente_bp
from database import Base, close_db_session, migrate


def create_app():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s [%(levelname)s %(name)s : %(message)s]"
    )

    app = Flask(__name__)
    migrate.init_app(app, Base.metadata)
    app.teardown_appcontext(close_db_session)
    app.register_blueprint(cliente_bp)
    app.register_blueprint(auto_blp)

    return app
