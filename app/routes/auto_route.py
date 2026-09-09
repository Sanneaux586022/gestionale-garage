import logging

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

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

@auto_blp.route("/auto/targa/<string:targa_auto>", methods=["GET"])
def get_auto_by_targa(targa_auto: str) -> dict:

    db_session = get_db_session()
    schema = AutoSchema()
    auto_service = AutoService(db_session, logger)

    try:
        auto = auto_service.cerca_auto_by_targa(targa_auto.upper())

        return jsonify({"response_data": schema.dump(auto)}), 200
    except NotFoundResultError as nfre:
        logger.warning(f"Warning: {nfre.message}")
        return jsonify({"errore": nfre.message}), nfre.status_code
    except Exception as err:
        logger.error(f"errore: {err}")
        return jsonify({"errore": "Errore durante l'operazione."}), 500    


@auto_blp.route("/auto/<int:id_auto>", methods=["PUT"])
def modify_auto(id_auto: int) -> dict:
    db_session = get_db_session()
    schema = AutoSchema()
    auto_service = AutoService(db_session, logger)

    try:
        data = schema.load(request.get_json())
    except ValidationError as val_err:
        logger.error(f"errore : {val_err}")
        return jsonify({"errore": "Dati inseriti non corretti."}), 400

    try:
        auto = auto_service.modifica_dati_auto(id_auto, data)
        return jsonify({"response_data": schema.dump(auto)}), 200
    except NotFoundResultError as nfre:
        logger.warning(f"Warning : {nfre.message}")
        return jsonify({"errore": nfre.message}), nfre.status_code
    except Exception as err:
        logger.error(f"errore: {err}")
        return jsonify({"errore": "Errore durante l'operazione."}), 500
