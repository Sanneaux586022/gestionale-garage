import logging

from flask import Blueprint, request
from marshmallow import ValidationError

from app.core.responses import *
from app.exceptions import InsufficientQuantityError, NotFoundResultError
from app.services.ricambio_service import RicambioService
from database import get_db_session
from schemas import RicambioQuantitaSchema, RicambioSchema

ricambio_blp = Blueprint("ricambio", __name__)
logger = logging.getLogger(f"{__name__}.RicambioRoute")


@ricambio_blp.route("/ricambio", methods=["POST"])
def add_ricambio():
    schema = RicambioSchema()
    db_session = get_db_session()
    ricambio_service = RicambioService(db_session, logger)

    try:
        data = schema.load(request.get_json())
    except ValidationError as val_err:
        logger.error(f"errore nei dati dal client: {val_err}.")
        return validation_error_response()

    try:
        ricambio = ricambio_service.aggiungi_ricambio(data)
        return ok_response(schema.dump(ricambio), 201)
    except Exception as err:
        logger.error(f"errore: {err}")
        return generic_error_response()


@ricambio_blp.route("/ricambio/<int:id_ricambio>", methods=["GET"])
def get_ricambio(id_ricambio: int) -> dict:
    db_session = get_db_session()
    schema = RicambioSchema()
    ricambio_service = RicambioService(db_session, logger)

    try:
        ricambio = ricambio_service.cerca_ricambio_by_id(id_ricambio)
        return ok_response(schema.dump(ricambio))
    except NotFoundResultError as nfre:
        logger.warning(f"Warning: {nfre.message}")
        return error_response(nfre.message, nfre.status_code)
    except Exception as err:
        logger.error(f"errore: {err}")
        return generic_error_response()


@ricambio_blp.route("/ricambio/<int:id_ricambio>", methods=["PUT"])
def modify_ricambio(id_ricambio: int) -> dict:
    schema = RicambioSchema()
    db_session = get_db_session()
    ricambio_service = RicambioService(db_session, logger)

    try:
        data = schema.load(request.get_json())
    except ValidationError as val_err:
        logger.error(f"errore nei dati dal client: {val_err}.")
        return validation_error_response()
    try:
        ricambio = ricambio_service.modifica_ricambio(id_ricambio, data)
        return ok_response(schema.dump(ricambio))
    except NotFoundResultError as nfre:
        logger.warning(f"Warning: {nfre.message}")
        return ok_response(nfre.message, nfre.status_code)
    except Exception as err:
        logger.error(f"errore: {err}")
        return generic_error_response()


@ricambio_blp.route("/ricambio/<int:id_ricambio>/scarico", methods=["PUT"])
def withdraw_ricambio(id_ricambio: int) -> dict:
    schema = RicambioQuantitaSchema()
    schema_ricambio = RicambioSchema()
    db_session = get_db_session()
    ricambio_service = RicambioService(db_session, logger)

    try:
        data = schema.load(request.get_json())
    except ValidationError as val_err:
        logger.error(f"errore nei dati dal client: {val_err}.")
        return validation_error_response()

    try:
        ricambio = ricambio_service.scarica_ricambio(id_ricambio, data["quantita"])
        return ok_response(schema_ricambio.dump(ricambio))
    except InsufficientQuantityError as iqe:
        logger.error(f"errore : {iqe.message}")
        return error_response(iqe.message, iqe.status_code)
    except NotFoundResultError as nfre:
        logger.warning(f"Warning: {nfre.message}")
        return error_response(nfre.message, nfre.status_code)
    except Exception as err:
        logger.error(f"errore: {err}")
        return generic_error_response()


@ricambio_blp.route("/ricambio/<int:id_ricambio>/carico", methods=["PUT"])
def stock_ricambio(id_ricambio: int) -> dict:
    schema = RicambioQuantitaSchema()
    schema_ricambio = RicambioSchema()
    db_session = get_db_session()
    ricambio_service = RicambioService(db_session, logger)

    try:
        data = schema.load(request.get_json())
    except ValidationError as val_err:
        logger.error(f"errore nei dati dal client: {val_err}.")
        return validation_error_response()
    try:
        ricambio = ricambio_service.carica_ricambio(id_ricambio, data["quantita"])
        return ok_response(schema_ricambio.dump(ricambio))

    except NotFoundResultError as nfre:
        logger.warning(f"Warning: {nfre.message}")
        return error_response(nfre.message, nfre.status_code)
    except Exception as err:
        logger.error(f"errore: {err}")
        return generic_error_response()
