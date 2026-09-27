import logging

from flask import Blueprint, request
from marshmallow import ValidationError

from app.core.responses import (
    error_response,
    generic_error_response,
    ok_response,
    validation_error_response,
)
from app.exceptions import ForbiddenOperationError, NotFoundResultError
from app.services.intervento_service import InterventoService
from database import get_db_session
from schemas.intervento_schema import (
    InterventoCompletatoSchema,
    InterventoNormaleResponseSchema,
    InterventoResponseSchema,
    InterventoSchema,
)

logger = logging.getLogger(f"{__name__}.InterventoRoute")
intervento_blp = Blueprint("Intervento", __name__)


@intervento_blp.route(
    "/auto/<int:id_auto>/meccanico/<int:id_meccanico>/intervento", methods=["POST"]
)
def create_intervento_urgente(id_auto: int, id_meccanico: int) -> dict:
    db_session = get_db_session()
    intervento_service = InterventoService(db_session, logger)
    schema = InterventoResponseSchema()
    try:
        intervento = intervento_service.crea_intervento_urgente(id_auto, id_meccanico)
        return ok_response(schema.dump(intervento), 201)
    except ForbiddenOperationError as foe:
        logger.error(f"errore: {foe.message}")
        return error_response(foe.message, foe.status_code)
    except NotFoundResultError as nfre:
        logger.warning(f"warning: {nfre.message}")
        return error_response(nfre.message, nfre.status_code)
    except Exception as err:
        logger.error(f"errore: {err}")
        return generic_error_response()


@intervento_blp.route(
    "/preventivo/<int:id_preventivo>/meccanico/<int:id_meccanico>/intervento",
    methods=["POST"],
)
def create_intervento(id_preventivo: int, id_meccanico: int) -> dict:
    db_session = get_db_session()
    intervento_service = InterventoService(db_session, logger)
    schema = InterventoNormaleResponseSchema()
    try:
        intervento = intervento_service.crea_intervento_da_preventivo(
            id_preventivo, id_meccanico
        )
        return ok_response(schema.dump(intervento), 201)
    except ForbiddenOperationError as foe:
        logger.error(f"errore: {foe.message}")
        return error_response(foe.message, foe.status_code)
    except NotFoundResultError as nfre:
        logger.warning(f"warning: {nfre.message}")
        return error_response(nfre.message, nfre.status_code)
    except Exception as err:
        logger.error(f"errore: {err}")
        return generic_error_response()


@intervento_blp.route("/intervento/<int:id_intervento>", methods=["GET"])
def get_intervento(id_intervento: int) -> dict:
    db_session = get_db_session()
    intervento_service = InterventoService(db_session, logger)
    schema = InterventoSchema()

    try:
        intervento = intervento_service.cerca_intervento_by_id(id_intervento)
        return ok_response(schema.dump(intervento))
    except NotFoundResultError as nfre:
        logger.warning(f"warning: {nfre.message}")
        return error_response(nfre.message, nfre.status_code)
    except Exception as err:
        logger.error(f"errore: {err}")
        return generic_error_response()


@intervento_blp.route("/intervento/<int:id_intervento>/completa", methods=["PUT"])
def complete_intervento(id_intervento: int) -> dict:
    db_session = get_db_session()
    schema_input = InterventoCompletatoSchema()
    schema_output = InterventoSchema()

    intervento_service = InterventoService(db_session, logger)
    try:
        data = schema_input.load(request.get_json())
    except ValidationError as val_err:
        logger.error(f"errore: {val_err}")
        return validation_error_response()

    try:
        intervento = intervento_service.completa_intervento(
            id_intervento, data["ore_lavorate"]
        )
        return ok_response(schema_output.dump(intervento))
    except ForbiddenOperationError as foe:
        logger.error(f"errore: {foe.message}")
        return error_response(foe.message, foe.status_code)
    except NotFoundResultError as nfre:
        logger.warning(f"warning: {nfre.message}")
        return error_response(nfre.message, nfre.status_code)
    except Exception as err:
        logger.error(f"errore: {err}")
        return generic_error_response()
