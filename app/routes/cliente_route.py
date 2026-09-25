import logging

from flask import Blueprint, request
from marshmallow import ValidationError

from app.core.responses import *
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
    except ValidationError as val_err:
        logger.error(f"errore nei dati dal client: {val_err}.")
        return validation_error_response()

    try:
        nuovo_cliente = cliente_service.aggiungi_cliente(data)
        return ok_response(schema.dump(nuovo_cliente), 201)

    except Exception as err:
        logger.error(f"Errore: {err}")
        return generic_error_response()


@cliente_bp.route("/cliente/<int:id_cliente>", methods=["GET"])
def get_cliente(id_cliente: int) -> dict:
    db_session = get_db_session()
    schema = ClienteSchema()
    cliente_service = ClienteService(db_session, logger)
    try:
        cliente = cliente_service.cerca_cliente_by_id(id_cliente)

        return ok_response(schema.dump(cliente))

    except NotFoundResultError as nfre:
        logger.warning(f"Warning: {nfre.message}")
        return error_response(nfre.message, nfre.status_code)
    except Exception as err:
        logger.error(f"errore: {err}")
        return generic_error_response()


@cliente_bp.route("/cliente/<int:id_cliente>", methods=["PUT"])
def modify_cliente(id_cliente):
    db_session = get_db_session()
    schema = ClienteSchema()
    cliente_service = ClienteService(db_session, logger)

    try:
        data = schema.load(request.get_json())
    except ValidationError as val_err:
        logger.error(f"errore nei dati dal client: {val_err}.")
        return validation_error_response()

    try:
        cliente = cliente_service.modifica_cliente(id_cliente, data)
        return ok_response(schema.dump(cliente))
    except NotFoundResultError as nfre:
        logger.warning(f"Warning : {nfre.message}")
        return error_response(nfre.message, nfre.status_code)
    except Exception as err:
        logger.error(f"errore: {err}")
        return generic_error_response()
