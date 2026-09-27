from decimal import Decimal

from sqlalchemy import CheckConstraint, ForeignKey, Identity, Numeric, text
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class InterventoRicambio(Base):

    __tablename__ = "intervento_ricambio"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    id_intervento: Mapped[int] = mapped_column(
        ForeignKey("intervento.id"), nullable=False
    )
    id_ricambio: Mapped[int] = mapped_column(ForeignKey("ricambio.id"), nullable=False)
    quantita_usata: Mapped[int] = mapped_column(nullable=False)
    prezzo_applicato: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    fatturabile: Mapped[bool] = mapped_column(
        nullable=False, server_default=text("true")
    )

    __table_args__ = (
        CheckConstraint(
            "quantita_usata >= 1",
            name="check_quantita_usata_minima",
        ),
    )
