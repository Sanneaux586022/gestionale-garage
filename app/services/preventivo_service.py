from sqlalchemy import and_, select
from sqlalchemy.exc import SQLAlchemyError

from app.core.service_base import ServiceBase
from app.core.utils import IN_ATTESA
from app.exceptions import ForbiddenOperationError, NotFoundResultError
from models import Preventivo, StoricoProprietaAuto


class PreventivoService(ServiceBase):

    def verifica_proprieta_attiva(self, id_cliente: int, id_auto: int) -> None:

        query = select(StoricoProprietaAuto).where(
            and_(
                StoricoProprietaAuto.id_cliente == id_cliente,
                StoricoProprietaAuto.id_auto == id_auto,
                StoricoProprietaAuto.data_fine.is_(None),
            )
        )
        storico = self.session.scalar(query)

        if not storico:
            raise NotFoundResultError(
                f"Non risulta nessuna auto con id : {id_auto},"
                f" di cui il cliente {id_cliente} è proprietario."
            )

    def crea_preventivo(self, id_cliente: int, id_auto: int, data: dict) -> Preventivo:

        try:
            self.verifica_proprieta_attiva(id_cliente, id_auto)
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
