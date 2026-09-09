from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.core.service_base import ServiceBase
from app.exceptions import NotFoundResultError
from models.auto_model import Auto
from models.storico_proprieta_auto_model import StoricoProprietaAuto


class AutoService(ServiceBase):

    def aggiungi_nuova_auto(self, id_cliente: int, dati_auto: dict) -> Auto:

        try:
            nuova_auto = Auto()
            for chiave, valore in dati_auto.items():
                setattr(nuova_auto, chiave, valore)

            self.session.add(nuova_auto)
            self.session.flush()

            storico_proprieta = StoricoProprietaAuto()
            storico_proprieta.id_auto = nuova_auto.id
            storico_proprieta.id_cliente = id_cliente

            self.session.add(storico_proprieta)
            self.session.commit()

            return nuova_auto

        except SQLAlchemyError as err:
            self.session.rollback()
            self.logger.error(f"Errore : {err}")
            raise

    def cerca_auto_by_id(self, id_auto: int) -> Auto:

        query = select(Auto).where(Auto.id == id_auto)

        result = self.session.scalar(query)

        if not result:
            raise NotFoundResultError(f"Nessuna auto trovata con l'id {id_auto}.")

        return result

    def cerca_auto_by_targa(self, targa: str) -> Auto:

        query = select(Auto).where(Auto.targa == targa)
        result = self.session.scalar(query)

        if not result:
            raise NotFoundResultError(f"Nessuna auto trovata con la targa: {targa}")

        return result

    def modifica_dati_auto(self, id_auto: int, dati_auto: dict) -> Auto:

        auto_da_modificare = self.cerca_auto_by_id(id_auto)

        try:

            for chiave, valore in dati_auto.items():
                setattr(auto_da_modificare, chiave, valore)

            self.session.commit()

            return auto_da_modificare
        except SQLAlchemyError as err:
            self.session.rollback()
            self.logger.error(f"errore: {err}")
            raise
