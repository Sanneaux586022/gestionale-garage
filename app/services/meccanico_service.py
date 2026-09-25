from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.core.service_base import ServiceBase
from app.exceptions import NotFoundResultError
from models import Meccanico


class MeccanicoService(ServiceBase):

    def aggiungi_meccanico(self, data: dict) -> Meccanico:
        try:
            nuovo_meccanico = Meccanico()

            for chiave, valore in data.items():
                setattr(nuovo_meccanico, chiave, valore)

            self.session.add(nuovo_meccanico)
            self.session.commit()
            return nuovo_meccanico
        except SQLAlchemyError as err:
            self.session.rollback()
            self.logger.error(f"errore : {err}.")
            raise

    def cerca_meccanico_by_id(self, id_meccanico: int) -> Meccanico:
        query = select(Meccanico).where(Meccanico.id == id_meccanico)

        result = self.session.scalar(query)

        if not result:
            raise NotFoundResultError(
                f"Nessun Meccanico trovato con l'id: {id_meccanico}."
            )

        return result

    def termina_rapporto(self, id_meccanico: int, data: dict) -> dict:

        try:
            meccanico = self.cerca_meccanico_by_id(id_meccanico)
            meccanico.data_fine_rapporto = data["data_fine_rapporto"]
            self.session.commit()
            return meccanico
        except SQLAlchemyError as err:
            self.session.rollback()
            self.logger.error(f"errore: {err}.")
            raise

    def modifica_meccanico(self, id_meccanico: int, data: dict) -> Meccanico:
        try:
            meccanico = self.cerca_meccanico_by_id(id_meccanico)

            for chiave, valore in data.items():
                setattr(meccanico, chiave, valore)
            self.session.commit()
            return meccanico
        except SQLAlchemyError as err:
            self.session.rollback()
            self.logger.error(f"errore: {err}.")
            raise
