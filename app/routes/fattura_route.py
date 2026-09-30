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
from app.services.fattura_service import FatturaService
from database import get_db_session
from schemas import (
    FatturaChiudiSchema,
    FatturaConImportoSchema,
    FatturaResponseSchema,
    InterventoSchema,
)

logger = logging.getLogger(f"{__name__}.FatturaRoute")
fattura_blp = Blueprint("Fattura", __name__)


@fattura_blp.route("/cliente/<int:id_cliente>/fattura", methods=["POST"])
def create_fattura(id_cliente: int) -> dict:
    db_session = get_db_session()
    schema = FatturaResponseSchema()
    fattura_service = FatturaService(db_session, logger)
    try:
        fattura = fattura_service.crea_fattura(id_cliente)
        return ok_response(schema.dump(fattura), 201)
    except NotFoundResultError as nfre:
        logger.warning(f"warning: {nfre.message}")
        return error_response(nfre.message, nfre.status_code)
    except Exception as err:
        logger.error(f"errore: {err}")
        return generic_error_response()


@fattura_blp.route("/fattura/<int:id_fattura>/chiudi", methods=["PUT"])
def close_fattura(id_fattura: int) -> dict:
    db_session = get_db_session()
    schema_output = FatturaResponseSchema()
    schema_input = FatturaChiudiSchema()
    fattura_service = FatturaService(db_session, logger)
    try:
        data = schema_input.load(request.get_json())
    except ValidationError as val_err:
        logger.error(f"errore: {val_err}")
        return validation_error_response()

    try:
        fattura = fattura_service.chiudi_fattura(id_fattura, data["data_pagamento"])
        return ok_response(schema_output.dump(fattura))
    except ForbiddenOperationError as foe:
        logger.warning(f"warning: {foe.message}")
        return error_response(foe.message, foe.status_code)
    except NotFoundResultError as nfre:
        logger.warning(f"warning: {nfre.message}")
        return error_response(nfre.message, nfre.status_code)
    except Exception as err:
        logger.error(f"errore: {err}")
        return generic_error_response()


@fattura_blp.route(
    "/fattura/<int:id_fattura>/intervento/<int:id_intervento>", methods=["PUT"]
)
def add_intervento_into_fattura(id_fattura: int, id_intervento: int) -> dict:
    db_session = get_db_session()
    fattura_service = FatturaService(db_session, logger)
    schema = InterventoSchema()

    try:
        intervento = fattura_service.aggancia_intervento(id_fattura, id_intervento)
        return ok_response(schema.dump(intervento))
    except NotFoundResultError as nfre:
        logger.warning(f"warning: {nfre.message}")
        return error_response(nfre.message, nfre.status_code)
    except ForbiddenOperationError as foe:
        logger.error(f"errore: {foe.message}")
        return error_response(foe.message, foe.status_code)
    except Exception as err:
        logger.error(f"errore: {err}")
        return generic_error_response()


@fattura_blp.route("/fattura/<int:id_fattura>", methods=["GET"])
def get_fattura_con_importo(id_fattura: int) -> dict:
    db_session = get_db_session()
    fattura_service = FatturaService(db_session, logger)
    schema = FatturaConImportoSchema()

    try:
        fattura_con_importo = fattura_service.cerca_fattura_con_importo_by_id(
            id_fattura
        )
        return ok_response(schema.dump(fattura_con_importo))
    except ForbiddenOperationError as foe:
        logger.error(f"errore: {foe.message}")
        return error_response(foe.message, foe.status_code)
    except NotFoundResultError as nfre:
        logger.error(f"errore: {nfre.message}")
        return error_response(nfre.message, nfre.status_code)
    except Exception as err:
        logger.error(f"errore : {err}")
        return generic_error_response()
