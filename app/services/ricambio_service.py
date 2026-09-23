from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.core.service_base import ServiceBase
from app.exceptions import NotFoundResultError, InsufficientQuantityError
from models import Ricambio


class RicambioService(ServiceBase):

    def aggiungi_ricambio(self, data: dict) -> Ricambio:
        try:
            ricambio = Ricambio()

            for chiave, valore in data.items():
                setattr(ricambio, chiave, valore)

            self.session.add(ricambio)
            self.session.commit()

            return ricambio
        except SQLAlchemyError as err:
            self.session.rollback()
            self.logger.error(f"errore: {err}")
            raise

    def cerca_ricambio_by_id(self, id_ricambio: int) -> Ricambio:

        query = select(Ricambio).where(Ricambio.id == id_ricambio)

        result = self.session.scalar(query)
        if not result:
            raise NotFoundResultError(
                f"Nessun Ricambio trovato con l'id: {id_ricambio}."
            )
        return result

    def modifica_ricambio(self, id_ricambio, data: dict)-> Ricambio:

        ricambio = self.cerca_ricambio_by_id(id_ricambio)
        try:
            for chiave, valore in data.items():
                setattr(ricambio, chiave, valore)
            self.session.commit()
            return ricambio
        except SQLAlchemyError as err:
            self.session.rollback()
            self.logger.error(f"errore: {err}")
            raise


    def scarica_ricambio(self, id_ricambio: int, quantita: int) -> Ricambio:
        try:
            ricambio = self.cerca_ricambio_by_id(id_ricambio)

            if ricambio.quantita_scorta < quantita:
                raise InsufficientQuantityError(
                    "L'operazione non può essere effettuata , scorta insufficiente."
                )
            ricambio.quantita_scorta = ricambio.quantita_scorta - quantita
            self.session.commit()
            return ricambio
        except SQLAlchemyError as err:
            self.session.rollback()
            self.logger.error(f"errore: {err}")
            raise

    
    def carica_ricambio(self, id_ricambio: int, quantita: int) -> Ricambio:
        try:
            ricambio = self.cerca_ricambio_by_id(id_ricambio)

            ricambio.quantita_scorta = ricambio.quantita_scorta + quantita
            self.session.commit()
            return ricambio
        except SQLAlchemyError as err:
            self.session.rollback()
            self.logger.error(f"errore: {err}")
            raise
        