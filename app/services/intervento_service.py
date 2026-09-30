from datetime import date
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.core.service_base import ServiceBase
from app.core.utils import ACCETTATO, COMPLETATO, IN_CORSO
from app.exceptions import ForbiddenOperationError, NotFoundResultError
from app.services.auto_service import AutoService
from app.services.meccanico_service import MeccanicoService
from app.services.preventivo_service import PreventivoService
from config import TARIFFA_ORARIA_STANDARD, TARIFFA_ORARIA_URGENZA
from models import Intervento


class InterventoService(ServiceBase):
    def crea_intervento_da_preventivo(
        self, id_preventivo: int, id_meccanico: int
    ) -> Intervento:
        preventivo_service = PreventivoService(self.session, self.logger)
        meccanico_service = MeccanicoService(self.session, self.logger)
        try:

            preventivo = preventivo_service.cerca_preventivo_by_id(id_preventivo)

            if preventivo.stato_preventivo != ACCETTATO:
                raise ForbiddenOperationError(
                    "Il preventivo deve essere in stato accettato per poter proseguire."
                )

            meccanico = meccanico_service.cerca_meccanico_by_id(id_meccanico)
            intervento_esistente = self.cerca_intervento_by_id_preventivo(id_preventivo)
            if intervento_esistente:
                raise ForbiddenOperationError(
                    f"il preventivo {id_preventivo} è già collegato ad un altro intervento."
                )
            intervento = Intervento(
                id_auto=preventivo.id_auto,
                id_meccanico=meccanico.id,
                id_cliente=preventivo.id_cliente,
                id_preventivo=preventivo.id,
                stato_intervento=IN_CORSO,
                tariffa_oraria_applicata=TARIFFA_ORARIA_STANDARD,
            )
            self.session.add(intervento)
            self.session.commit()
            return intervento
        except SQLAlchemyError as err:
            self.session.rollback()
            self.logger.error(f"errore: {err}")
            raise

    def crea_intervento_urgente(
        self, id_auto: int, id_meccanico: int, id_cliente: int
    ) -> Intervento:
        meccanico_service = MeccanicoService(self.session, self.logger)
        auto_service = AutoService(self.session, self.logger)
        try:
            meccanico = meccanico_service.cerca_meccanico_by_id(id_meccanico)
            auto = auto_service.cerca_auto_by_id(id_auto)
            auto_service.verifica_proprieta_attiva(id_cliente=id_cliente, id_auto=id_auto)
            intervento = Intervento(
                id_auto=auto.id,
                id_meccanico=meccanico.id,
                id_cliente=id_cliente,
                stato_intervento=IN_CORSO,
                tariffa_oraria_applicata=TARIFFA_ORARIA_URGENZA,
            )
            self.session.add(intervento)
            self.session.commit()
            return intervento
        except SQLAlchemyError as err:
            self.logger.error(f"errore: {err}")
            self.session.rollback()
            raise

    def cerca_intervento_by_id_preventivo(self, id_preventivo: int) -> Intervento:

        query = select(Intervento).where(Intervento.id_preventivo == id_preventivo)
        intervento = self.session.scalar(query)

        return intervento

    def cerca_intervento_by_id(self, id_intervento: int) -> Intervento:

        query = select(Intervento).where(Intervento.id == id_intervento)
        intervento = self.session.scalar(query)

        if not intervento:
            raise NotFoundResultError(
                f"Nessun intervento trovato con l'id {id_intervento}"
            )

        return intervento

    def completa_intervento(
        self, id_intervento: int, ore_lavorate: Decimal
    ) -> Intervento:
        try:
            intervento = self.cerca_intervento_by_id(id_intervento)

            if intervento.stato_intervento != IN_CORSO:
                raise ForbiddenOperationError(
                    f"L'intervento deve essere in stato {IN_CORSO} per poterlo chiudere."
                )

            intervento.data_fine_intervento = date.today()
            intervento.ore_lavorate = ore_lavorate
            intervento.stato_intervento = COMPLETATO
            self.session.commit()
            return intervento
        except SQLAlchemyError as err:
            self.logger.error(f"errore: {err}")
            self.session.rollback()
            raise

    def cerca_intervento_by_id_fattura(self, id_fattura: int) -> list[Intervento]:

        query = select(Intervento).where(Intervento.id_fattura == id_fattura)

        interventi = self.session.scalars(query)

        return list(interventi)
