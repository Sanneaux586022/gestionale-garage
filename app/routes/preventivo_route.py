import logging

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from app.exceptions import NotFoundResultError
from app.services.preventivo_service import PreventivoService
from database import get_db_session
from schemas import PreventivoSchema

preventivo_blp = Blueprint("Preventivo", __name__)
logger = logging.getLogger(f"{__name__}.PreventivoRoute")


@preventivo_blp.route(
    "/cliente/<int:id_cliente>/auto/<int:id_auto>/preventivo", methods=["POST"]
)
def add_preventivo(id_cliente: int, id_auto: int) -> dict:
    schema = PreventivoSchema()
    db_session = get_db_session()
    preventivo_service = PreventivoService(db_session, logger)

    try:
        data = schema.load(request.get_json())
    except ValidationError as val_err:
        logger.error(f"errore: {val_err}")
        return jsonify({"errore": "Dati inseriti non corretti."}), 400

    try:
        preventivo = preventivo_service.crea_preventivo(id_cliente, id_auto, data)
        return jsonify({"response_data": schema.dump(preventivo)}), 201
    except NotFoundResultError as nfre:
        logger.warning(f"Warning : {nfre.message}")
        return jsonify({"errore": nfre.message}), nfre.status_code
    except Exception as err:
        logger.error(f"errore: {err}")
        return jsonify({"errore": "Errore durante l'operazione di creazione."}), 500
