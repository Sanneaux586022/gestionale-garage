from sqlalchemy import select

from app.core.service_base import ServiceBase
from app.exceptions import NotFoundResultError
from models.cliente_model import Cliente


class ClienteService(ServiceBase):

    def aggiungi_cliente(self, dati_cliente: dict) -> int:

        try:
            nuovo_cliente = Cliente(
                nome=dati_cliente["nome"],
                cognome=dati_cliente["cognome"],
                telefono=dati_cliente["telefono"],
                email=dati_cliente.get("email"),
            )
            self.session.add(nuovo_cliente)
            self.session.commit()
            return nuovo_cliente
        except Exception as err:
            self.session.rollback()
            self.logger.error(f"Errore : {err}")
            raise

    def cerca_cliente_by_id(self, id_cliente: int) -> Cliente:

        query = select(Cliente).where(Cliente.id == id_cliente)
        result = self.session.scalar(query)

        if not result:
            raise NotFoundResultError(f"Nessun utente trovato con l'id: {id_cliente}")

        return result
