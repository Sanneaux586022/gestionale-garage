from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.core.service_base import ServiceBase
from app.core.utils import IN_CORSO
from app.exceptions import ForbiddenOperationError, NotFoundResultError
from app.services.intervento_service import InterventoService
from app.services.ricambio_service import RicambioService
from models import InterventoRicambio


class InterventoRicambioService(ServiceBase):
    def registra_ricambio_su_intervento(
        self, id_intervento: int, id_ricambio: int, data: dict
    ) -> InterventoRicambio:
        intervento_service = InterventoService(self.session, self.logger)
        ricambio_service = RicambioService(self.session, self.logger)

        try:

            intervento = intervento_service.cerca_intervento_by_id(id_intervento)
            if intervento.stato_intervento != IN_CORSO:
                raise ForbiddenOperationError(
                    f"L'intervento deve in stato {IN_CORSO} per poter proseguire."
                )
            ricambio = ricambio_service.cerca_ricambio_by_id(id_ricambio)
            ricambio_scaricato = ricambio_service.scarica_ricambio(
                ricambio.id, data["quantita_usata"]
            )
            intervento_ricambio = InterventoRicambio(
                id_intervento=intervento.id,
                id_ricambio=ricambio_scaricato.id,
                prezzo_applicato=ricambio_scaricato.prezzo_vendita,
                quantita_usata=data["quantita_usata"],
                fatturabile=data["fatturabile"],
            )
            self.session.add(intervento_ricambio)
            self.session.commit()
            return intervento_ricambio

        except SQLAlchemyError as err:
            self.session.rollback()
            self.logger.error(f"errore: {err}")
            raise

    def cerca_intervento_ricambio_by_id(
        self, id_intervento_ricambio: int
    ) -> InterventoRicambio:

        query = select(InterventoRicambio).where(
            InterventoRicambio.id == id_intervento_ricambio
        )

        intervento_ricambio = self.session.scalar(query)

        if not intervento_ricambio:
            raise NotFoundResultError(
                f"Nessun intervento_ricambio trovato con l'id {id_intervento_ricambio}."
            )

        return intervento_ricambio

    def cerca_ricambi_by_intervento(self, id_intervento: int) -> list[InterventoRicambio]:

        query = select(InterventoRicambio).where(InterventoRicambio.id_intervento == id_intervento)

        interventi = self.session.scalars(query)
        return list(interventi)