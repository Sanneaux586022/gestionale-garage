import logging

from flask import Blueprint

from app.core.responses import error_response, generic_error_response, ok_response
from app.exceptions import ForbiddenOperationError, NotFoundResultError
from app.services.intervento_service import InterventoService
from database import get_db_session
from schemas.intervento_schema import (
    InterventoNormaleResponseSchema,
    InterventoResponseSchema,
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
        logger.error(f"errore: {nfre.message}")
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
        logger.error(f"errore: {nfre.message}")
        return error_response(nfre.message, nfre.status_code)
    except Exception as err:
        logger.error(f"errore: {err}")
        return generic_error_response()
