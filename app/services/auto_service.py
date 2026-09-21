from datetime import date

from sqlalchemy import and_, select
from sqlalchemy.exc import SQLAlchemyError

from app.core.service_base import ServiceBase
from app.exceptions import NotFoundResultError
from app.services.cliente_service import ClienteService
from models import Auto, StoricoProprietaAuto


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

    def get_info_auto_by_id(self, id_auto: int) -> dict:
        pass

    def cambio_proprieta(self, id_auto: int, id_cliente_new: int) -> dict:
        cliente_service = ClienteService(self.session, self.logger)

        auto = self.cerca_auto_by_id(id_auto)

        query = select(StoricoProprietaAuto).where(
            and_(
                StoricoProprietaAuto.id_auto == id_auto,
                StoricoProprietaAuto.data_fine.is_(None),
            )
        )
        dati_proprieta = self.session.scalar(query)
        if not dati_proprieta:
            raise NotFoundResultError(
                f"Nessun dato di proprieta attivo per questa auto : {auto.targa}."
            )

        precedente_prorietario = cliente_service.cerca_cliente_by_id(
            dati_proprieta.id_cliente
        )

        nuovo_proprietario = cliente_service.cerca_cliente_by_id(id_cliente_new)


        try:
            dati_proprieta.data_fine = date.today()
            self.session.flush()
            new_dati_prorpieta = StoricoProprietaAuto(
                id_cliente=id_cliente_new,
                id_auto=id_auto,
            )
            self.session.add(new_dati_prorpieta)
            self.session.commit()
            return {
                "nome_cliente": nuovo_proprietario.nome,
                "id_cliente": new_dati_prorpieta.id_cliente,
                "targa": auto.targa,
                "precedente_proprietario": precedente_prorietario.nome
            }
        except SQLAlchemyError as err:
            self.session.rollback()
            self.logger.error(f"errore: {err}")
            raise
