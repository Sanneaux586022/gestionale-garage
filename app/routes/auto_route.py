import logging

from flask import Blueprint, request
from marshmallow import ValidationError

from app.core.responses import *
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

        return ok_response(schema.dump(auto))
    except NotFoundResultError as nfre:
        logger.warning(f"Warning: {nfre.message}")
        return error_response(nfre.message, nfre.status_code)
    except Exception as err:
        logger.error(f"errore: {err}")
        return generic_error_response()


@auto_blp.route("/auto/targa/<string:targa_auto>", methods=["GET"])
def get_auto_by_targa(targa_auto: str) -> dict:

    db_session = get_db_session()
    schema = AutoSchema()
    auto_service = AutoService(db_session, logger)

    try:
        auto = auto_service.cerca_auto_by_targa(targa_auto.upper())

        return ok_response(schema.dump(auto))
    except NotFoundResultError as nfre:
        logger.warning(f"Warning: {nfre.message}")
        return error_response(nfre.message, nfre.status_code)
    except Exception as err:
        logger.error(f"errore: {err}")
        return generic_error_response()


@auto_blp.route("/auto/<int:id_auto>", methods=["PUT"])
def modify_auto(id_auto: int) -> dict:
    db_session = get_db_session()
    schema = AutoSchema()
    auto_service = AutoService(db_session, logger)

    try:
        data = schema.load(request.get_json())
    except ValidationError as val_err:
        logger.error(f"errore : {val_err}")
        return validation_error_response()

    try:
        auto = auto_service.modifica_dati_auto(id_auto, data)
        return ok_response(schema.dump(auto))
    except NotFoundResultError as nfre:
        logger.warning(f"Warning : {nfre.message}")
        return error_response(nfre.message, nfre.status_code)
    except Exception as err:
        logger.error(f"errore: {err}")
        return generic_error_response()


@auto_blp.route(
    "/auto/<int:id_auto>/storico_proprieta/<int:id_cliente>", methods=["PUT"]
)
def cambio_proprietario(id_auto: int, id_cliente: int):
    db_session = get_db_session()

    auto_service = AutoService(db_session, logger)
    try:
        nuovo_proprietario = auto_service.cambio_proprieta(id_auto, id_cliente)
        return ok_response(nuovo_proprietario)

    except NotFoundResultError as nfre:
        logger.warning(f"Warning : {nfre.message}")
        return error_response(nfre.message, nfre.status_code)
    except Exception as err:
        logger.error(f"errore: {err}")
        return generic_error_response()


@auto_blp.route("/cliente/<int:id_cliente>/auto", methods=["POST"])
def aggiungi_auto_a_cliente(id_cliente):
    db_session = get_db_session()
    schema = AutoSchema()
    auto_service = AutoService(db_session, logger)

    try:
        data = schema.load(request.get_json())
    except ValidationError as val_err:
        logger.error(f"errore nei dati dal client: {val_err}.")
        return validation_error_response()

    try:
        auto = auto_service.aggiungi_nuova_auto(id_cliente, data)

        return ok_response(schema.dump(auto), 201)

    except NotFoundResultError as nfre:
        logger.warning(f"Warning: {nfre.message}")
        return error_response(nfre.message, nfre.status_code)
    except Exception as err:
        logger.error(f"errore: {err}.")
        return generic_error_response()
