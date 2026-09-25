import logging

from flask import Blueprint, request
from marshmallow import ValidationError

from app.core.responses import *
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
        return validation_error_response()

    try:
        preventivo = preventivo_service.crea_preventivo(id_cliente, id_auto, data)
        return ok_response(schema.dump(preventivo), 201)
    except NotFoundResultError as nfre:
        logger.warning(f"Warning : {nfre.message}")
        return error_response(nfre.message, nfre.status_code)
    except Exception as err:
        logger.error(f"errore: {err}")
        return generic_error_response()
