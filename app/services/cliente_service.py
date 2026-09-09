from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.core.service_base import ServiceBase
from app.exceptions import NotFoundResultError
from models.cliente_model import Cliente


class ClienteService(ServiceBase):

    def aggiungi_cliente(self, dati_cliente: dict) -> Cliente:

        try:
            nuovo_cliente = Cliente()

            for chiave, valore in dati_cliente.items():
                setattr(nuovo_cliente, chiave, valore)

            self.session.add(nuovo_cliente)
            self.session.commit()
            return nuovo_cliente
        except SQLAlchemyError as err:
            self.session.rollback()
            self.logger.error(f"Errore : {err}")
            raise

    def cerca_cliente_by_id(self, id_cliente: int) -> Cliente:

        query = select(Cliente).where(Cliente.id == id_cliente)
        result = self.session.scalar(query)

        if not result:
            raise NotFoundResultError(f"Nessun utente trovato con l'id: {id_cliente}.")

        return result

    def modifica_cliente(self, id_cliente: int, dati_cliente: dict) -> Cliente:

        cliente_da_modificare = self.cerca_cliente_by_id(id_cliente)

        try:
            for chiave, valore in dati_cliente.items():
                setattr(cliente_da_modificare, chiave, valore)

            self.session.commit()
            return cliente_da_modificare
        except SQLAlchemyError as err:
            self.session.rollback()
            self.logger.error(f"errore: {err}")
            raise

    def elimina_cliente(self, id_cliente: int):
        pass
