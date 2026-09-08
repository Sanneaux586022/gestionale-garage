from sqlalchemy.exc import SQLAlchemyError

from app.core.service_base import ServiceBase
from models.auto import Auto
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
