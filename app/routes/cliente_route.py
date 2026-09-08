import logging

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from app.exceptions import NotFoundResultError
from app.services.cliente_service import ClienteService
from database import get_db_session
from schemas.cliente_schema import ClienteSchema

cliente_bp = Blueprint("cliente", __name__)
logger = logging.getLogger(f"{__name__}.ClienteRoute")


@cliente_bp.route("/cliente", methods=["POST"])
def add_cliente() -> dict:

    db_session = get_db_session()
    schema = ClienteSchema()
    cliente_service = ClienteService(db_session, logger)
    try:
        data = schema.load(request.get_json())
    except ValidationError as err:
        logger.error(f"errore nei dati dal client: {err}")
        return jsonify({"errore": "Dati inseriti non corretti."}), 400

    try:
        nuovo_cliente = cliente_service.aggiungi_cliente(data)
        return (
            jsonify(
                {
                    "message": f"utente {nuovo_cliente.nome}, con id {nuovo_cliente.id} correttamente generato"
                }
            ),
            201,
        )

    except Exception as err:
        logger.error(f"Errore: {err}")
        return jsonify({"errore": "Errore durante l'operazione"}), 500


@cliente_bp.route("/cliente/<int:id_cliente>", methods=["GET"])
def get_cliente(id_cliente: int) -> dict:
    db_session = get_db_session()
    schema = ClienteSchema()
    cliente_service = ClienteService(db_session, logger)
    try:
        cliente = cliente_service.cerca_cliente_by_id(id_cliente)

        return jsonify({"response_data": schema.dump(cliente)}), 200

    except NotFoundResultError as nfre:
        logger.warning(f"Warning: {nfre.message}")
        return jsonify({"errore": nfre.message}), nfre.status_code
    except Exception as err:
        logger.error(f"errore: {err}")
        return jsonify({"errore": "Errore durante l'operazione"}), 500


@cliente_bp.route("/cliente/<int:id_cliente>", methods=["PUT"])
def modify_cliente(id_cliente):
    db_session = get_db_session()
    schema = ClienteSchema()
    cliente_service = ClienteService(db_session, logger)

    try:
        data = schema.load(request.get_json())
    except ValidationError as err:
        logger.error(f"errore nei dati dal client: {err}")
        return jsonify({"errore": "Dati inseriti non corretti."}), 400

    try:
        cliente = cliente_service.modifica_cliente(id_cliente, data)
        return jsonify({"response_data": schema.dump(cliente)}), 200
    except NotFoundResultError as nfre:
        logger.warning(f"Warning : {nfre.message}")
        return jsonify({"errore": nfre.message}), nfre.status_code
    except Exception as err:
        logger.error(f"errore: {err}")
        return jsonify({"errore": "Errore durante l'operazione di modifica"}), 500
