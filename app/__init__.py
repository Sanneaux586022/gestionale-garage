from flask import Flask
from routes.cliente import cliente_bp

from database import close_db_session


def create_app():

    app = Flask(__name__)

    app.teardown_appcontext(close_db_session)
    app.register_blueprint(cliente_bp)

    return app
