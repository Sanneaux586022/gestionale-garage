from sqlalchemy import and_, select
from sqlalchemy.exc import SQLAlchemyError
from app.core.service_base import ServiceBase
from app.exceptions import NotFoundResultError
from models import StoricoProprietaAuto, Preventivo


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

    def crea_preventivo(self, id_cliente: int, id_auto: int, data: dict)-> Preventivo:

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

