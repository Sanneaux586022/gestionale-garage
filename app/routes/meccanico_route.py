import logging

from flask import Blueprint, request
from marshmallow import ValidationError

from app.core.responses import *
from app.exceptions import NotFoundResultError
from app.services.meccanico_service import MeccanicoService
from database import get_db_session
from schemas import CancelMeccanicoSchema, MeccanicoSchema, MeccanicoSchemaResponse

meccanico_blp = Blueprint("meccanico", __name__)
logger = logging.getLogger(f"{__name__}.MeccanicoRoute")


@meccanico_blp.route("/meccanico", methods=["POST"])
def add_meccanico():
    db_session = get_db_session()
    schema = MeccanicoSchema()
    meccanico_service = MeccanicoService(db_session, logger)

    try:
        data = schema.load(request.get_json())
    except ValidationError as val_err:
        logger.error(f"errore nei dati dal client: {val_err}.")
        return validation_error_response()

    try:
        meccanico = meccanico_service.aggiungi_meccanico(data)
        return ok_response(schema.dump(meccanico), 201)
    except Exception as err:
        logger.error(f"Errore: {err}")
        return generic_error_response()


@meccanico_blp.route("/meccanico/<int:id_meccanico>/fine_rapporto", methods=["PUT"])
def cancel_meccanico(id_meccanico: int) -> dict:
    schema = CancelMeccanicoSchema()
    schema_response = MeccanicoSchemaResponse()
    db_session = get_db_session()
    meccanico_service = MeccanicoService(db_session, logger)
    try:
        data = schema.load(request.get_json())
    except ValidationError as val_err:
        logger.error(f"errore nei dati dal client: {val_err}")
        return validation_error_response()
    try:
        meccanico = meccanico_service.termina_rapporto(id_meccanico, data)
        return ok_response(schema_response.dump(meccanico))
    except NotFoundResultError as nfre:
        logger.warning(f"Warning: {nfre.message}")
        return error_response(nfre.message, nfre.status_code)
    except Exception as err:
        logger.error(f"errore: {err}")
        return generic_error_response()


@meccanico_blp.route("/meccanico/<int:id_meccanico>", methods=["GET"])
def get_meccanico(id_meccanico: int) -> dict:
    db_session = get_db_session()
    meccanico_service = MeccanicoService(db_session, logger)
    schema = MeccanicoSchemaResponse()
    try:
        meccanico = meccanico_service.cerca_meccanico_by_id(id_meccanico)
        return ok_response(schema.dump(meccanico))
    except NotFoundResultError as nfre:
        logger.warning(f"Warning: {nfre.message}")
        return error_response(nfre.message, nfre.status_code)
    except Exception as err:
        logger.error(f"errore: {err}")
        return generic_error_response()


@meccanico_blp.route("/meccanico/<int:id_meccanico>", methods=["PUT"])
def modify_meccanico(id_meccanico: int) -> dict:
    db_session = get_db_session()
    schema = MeccanicoSchema()
    schema_response = MeccanicoSchemaResponse()
    meccanico_service = MeccanicoService(db_session, logger)

    try:
        data = schema.load(request.get_json())
    except ValidationError as val_err:
        logger.error(f"errore nei dati dal client: {val_err}")
        return validation_error_response()

    try:
        meccanico = meccanico_service.modifica_meccanico(id_meccanico, data)
        return ok_response(schema_response.dump(meccanico))
    except NotFoundResultError as nfre:
        logger.warning(f"Warning: {nfre.message}")
        return error_response(nfre.message, nfre.status_code)
    except Exception as err:
        logger.error(f"errore: {err}")
        return generic_error_response()
