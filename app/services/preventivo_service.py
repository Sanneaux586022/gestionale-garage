from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.core.service_base import ServiceBase
from app.core.utils import IN_ATTESA
from app.exceptions import ForbiddenOperationError, NotFoundResultError
from app.services.auto_service import AutoService
from models import Preventivo


class PreventivoService(ServiceBase):

    def crea_preventivo(self, id_cliente: int, id_auto: int, data: dict) -> Preventivo:
        auto_service = AutoService(self.session, self.logger)
        try:
            auto_service.verifica_proprieta_attiva(id_cliente, id_auto)
            preventivo = Preventivo()

            for chiave, valore in data.items():
                setattr(preventivo, chiave, valore)

            preventivo.id_cliente = id_cliente
            preventivo.id_auto = id_auto
            preventivo.stato_preventivo = "in_attesa"
            self.session.add(preventivo)
            self.session.commit()
            return preventivo
        except SQLAlchemyError as err:
            self.session.rollback()
            self.logger.error(f"errore: {err}")
            raise

    def cerca_preventivo_by_id(self, id_preventivo: int) -> Preventivo:
        query = select(Preventivo).where(Preventivo.id == id_preventivo)
        preventivo = self.session.scalar(query)

        if not preventivo:
            raise NotFoundResultError(
                f"Nessun preventivo trovato con l'id : {id_preventivo}"
            )
        return preventivo

    def cambia_stato_preventivo(
        self, id_preventivo: int, nuovo_stato: str
    ) -> Preventivo:
        preventivo = self.cerca_preventivo_by_id(id_preventivo)

        if preventivo.stato_preventivo != IN_ATTESA:
            raise ForbiddenOperationError(
                "Il preventivo deve essere nello stato 'in attesa'."
            )

        try:
            preventivo.stato_preventivo = nuovo_stato
            self.session.commit()
            return preventivo
        except SQLAlchemyError as err:
            self.session.rollback()
            self.logger.error(f"errore: {err}")
            raise
