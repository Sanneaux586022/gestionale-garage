from sqlalchemy.exc import SQLAlchemyError

from app.core.service_base import ServiceBase
from app.core.utils import ACCETTATO, IN_CORSO
from app.exceptions import ForbiddenOperationError
from app.services.meccanico_service import MeccanicoService
from app.services.preventivo_service import PreventivoService
from app.services.auto_service import AutoService
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
            intervento = Intervento(
                id_auto=preventivo.id_auto,
                id_meccanico=meccanico.id,
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

    def crea_intervento_urgente(self, id_auto: int, id_meccanico: int) -> Intervento:
        meccanico_service = MeccanicoService(self.session, self.logger)
        auto_service = AutoService(self.session, self.logger)
        try:
            meccanico = meccanico_service.cerca_meccanico_by_id(id_meccanico)
            auto = auto_service.cerca_auto_by_id(id_auto)
            intervento = Intervento(
                id_auto=auto.id,
                id_meccanico=meccanico.id,
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