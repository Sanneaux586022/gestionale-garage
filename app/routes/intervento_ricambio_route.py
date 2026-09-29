import logging

from flask import Blueprint, request
from marshmallow import ValidationError

from app.core.responses import (
    error_response,
    generic_error_response,
    ok_response,
    validation_error_response,
)
from app.exceptions import (
    ForbiddenOperationError,
    InsufficientQuantityError,
    NotFoundResultError,
)
from app.services.intervento_ricambio_service import InterventoRicambioService
from database import get_db_session
from schemas import InterventoRicambioResponseSchema, InterventoRicambioSchema

intervento_ricambio_blp = Blueprint("InterventoRicambio", __name__)
logger = logging.getLogger(f"{__name__}.InterventoRicambio")


@intervento_ricambio_blp.route(
    "/intervento_ricambio/<int:id_intervento>/ricambio/<int:id_ricambio>",
    methods=["POST"],
)
def create_intervento_ricambio(id_intervento: int, id_ricambio: int) -> dict:
    db_session = get_db_session()
    intervento_ricambio_service = InterventoRicambioService(db_session, logger)
    schema_input = InterventoRicambioSchema()
    schema_ouput = InterventoRicambioResponseSchema()

    try:
        data = schema_input.load(request.get_json())
    except ValidationError as val_err:
        logger.warning(f"warning: {val_err}")
        return validation_error_response()

    try:
        intervento_ricambio = (
            intervento_ricambio_service.registra_ricambio_su_intervento(
                id_intervento, id_ricambio, data
            )
        )
        return ok_response(schema_ouput.dump(intervento_ricambio), 201)
    except InsufficientQuantityError as iqe:
        logger.error(f"errore: {iqe.message}")
        return error_response(iqe.message, iqe.status_code)
    except NotFoundResultError as nfre:
        logger.error(f"errore: {nfre.message}")
        return error_response(nfre.message, nfre.status_code)
    except ForbiddenOperationError as foe:
        logger.error(f"errore: {foe.message}")
        return error_response(foe.message, foe.status_code)
    except Exception as err:
        logger.error(f"errore: {err}")
        return generic_error_response()


@intervento_ricambio_blp.route(
    "/intervento_ricambio/<int:id_intervento_ricambio>", methods=["GET"]
)
def get_intervento_ricambio(id_intervento_ricambio: int) -> dict:
    db_session = get_db_session()
    intervento_ricambio_service = InterventoRicambioService(db_session, logger)
    schema = InterventoRicambioResponseSchema()
    try:
        intervento_ricambio = (
            intervento_ricambio_service.cerca_intervento_ricambio_by_id(
                id_intervento_ricambio
            )
        )
        return ok_response(schema.dump(intervento_ricambio))
    except NotFoundResultError as nfre:
        logger.warning(f"warning: {nfre.message}")
        return error_response(nfre.message, nfre.status_code)
    except Exception as err:
        logger.error(f"errore: {err}")
        return generic_error_response()
