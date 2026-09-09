import logging

from flask import Blueprint, jsonify

from app.exceptions import NotFoundResultError
from app.services.auto_service import AutoService
from database import get_db_session
from schemas.auto_schema import AutoSchema

auto_blp = Blueprint("auto", __name__)

logger = logging.getLogger(f"{__name__}.AutoRoute")


@auto_blp.route("/auto/<int:id_auto>", methods=["GET"])
def get_auto(id_auto: int) -> dict:

    db_session = get_db_session()
    schema = AutoSchema()
    auto_service = AutoService(db_session, logger)

    try:
        auto = auto_service.cerca_auto_by_id(id_auto)

        return jsonify({"response_data": schema.dump(auto)}), 200
    except NotFoundResultError as nfre:
        logger.warning(f"Warning: {nfre.message}")
        return jsonify({"errore": nfre.message}), nfre.status_code
    except Exception as err:
        logger.error(f"errore: {err}")
        return jsonify({"errore": "Errore durante l'operazione."}), 500
