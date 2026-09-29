from datetime import date, timedelta
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.core.service_base import ServiceBase
from app.core.utils import COMPLETATO
from app.exceptions import ForbiddenOperationError, NotFoundResultError
from app.services.cliente_service import ClienteService
from app.services.intervento_ricambio_service import InterventoRicambioService
from app.services.intervento_service import InterventoService
from config import GIORNI_SCADENZA_FATTURA
from models import Fattura, Intervento


class FatturaService(ServiceBase):
    def crea_fattura(self, id_cliente: int) -> Fattura:
        cliente_service = ClienteService(self.session, self.logger)
        try:
            cliente = cliente_service.cerca_cliente_by_id(id_cliente)
            fattura = Fattura(
                id_cliente=cliente.id,
                data_scadenza=date.today() + timedelta(days=GIORNI_SCADENZA_FATTURA),
            )
            self.session.add(fattura)
            self.session.commit()
            return fattura
        except SQLAlchemyError as err:
            self.session.rollback()
            self.logger.error(f"errore: {err}")
            raise

    def chiudi_fattura(self, id_fattura: int, data_chiusura: date) -> Fattura:
        try:
            fattura = self.cerca_fattura_by_id(id_fattura)
            if fattura.data_pagamento is not None:
                raise ForbiddenOperationError("La fattura è già stata pagata.")
            if fattura.data_emissione > data_chiusura:
                raise ForbiddenOperationError(
                    "La data di pagamento non può essere precedente alla data di emissione."
                )
            fattura.data_pagamento = data_chiusura
            self.session.commit()
            return fattura
        except SQLAlchemyError as err:
            self.session.rollback()
            self.logger.error(f"errore: {err}")
            raise

    def cerca_fattura_by_id(self, id_fattura: int) -> Fattura:
        query = select(Fattura).where(Fattura.id == id_fattura)

        fattura = self.session.scalar(query)

        if not fattura:
            raise NotFoundResultError(f"Nessuna fattura trovata con l'id {id_fattura}")
        return fattura

    def aggancia_intervento(self, id_fattura: int, id_intervento: int) -> Intervento:
        intervento_service = InterventoService(self.session, self.logger)
        try:
            fattura = self.cerca_fattura_by_id(id_fattura)
            if fattura.data_pagamento:
                raise ForbiddenOperationError(
                    f"Impossibile aggiungere intervento: fattura già pagata in data {fattura.data_pagamento}."
                )
            intervento = intervento_service.cerca_intervento_by_id(id_intervento)
            if intervento.stato_intervento != COMPLETATO:
                raise ForbiddenOperationError(
                    f"Impossibile aggiungere un intervento in stato {intervento.stato_intervento}."
                )
            if intervento.id_fattura:
                raise ForbiddenOperationError(
                    f"Impossibile aggiungere un intervento presente in un'altra fattura {intervento.id_fattura}."
                )
            if fattura.id_cliente != intervento.id_cliente:
                raise ForbiddenOperationError(
                    f"Impossibile agganciare intervento lìintervento: {intervento.id}. I clineti non corrispondono."
                )
            intervento.id_fattura = fattura.id
            self.session.commit()
            return intervento

        except SQLAlchemyError as err:
            self.session.rollback()
            self.logger.error(f"errore: {err}")
            raise

    def calcola_importo_intervento(self, id_intervento: int) -> Decimal:
        intervento_service = InterventoService(self.session, self.logger)
        intervento_ricambio_service = InterventoRicambioService(
            self.session, self.logger
        )

        importo_ricambi = Decimal(0)
        manodopera = Decimal(0)
        intervento = intervento_service.cerca_intervento_by_id(id_intervento)
        if intervento.stato_intervento != COMPLETATO:
            raise ForbiddenOperationError("Intervento non in stato completato.")
        manodopera += Decimal(
            intervento.ore_lavorate * intervento.tariffa_oraria_applicata
        )
        ricambi = intervento_ricambio_service.cerca_ricambi_by_intervento(intervento.id)
        ricambi_intervento = [
            ricambio for ricambio in ricambi if ricambio.fatturabile == True
        ]
        importo_ricambi += Decimal(
            sum(
                [
                    ricambio.quantita_usata * ricambio.prezzo_applicato
                    for ricambio in ricambi_intervento
                ]
            )
        )
        return manodopera + importo_ricambi

    def calcola_importo_fattura(self, id_fattura: int) -> Decimal:
        intervento_service = InterventoService(self.session, self.logger)
        importo_fattura = Decimal(0)
        interventi = intervento_service.cerca_intervento_by_id_fattura(id_fattura)

        for intervento in interventi:
            importo_fattura += self.calcola_importo_intervento(intervento.id)

        return importo_fattura

    def cerca_fattura_con_importo_by_id(self, id_fattura: int) -> dict:
        fattura = self.cerca_fattura_by_id(id_fattura)

        importo_totale = self.calcola_importo_fattura(id_fattura)

        return {"fattura": fattura, "importo_totale": importo_totale}
