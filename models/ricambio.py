from decimal import Decimal

from sqlalchemy import CheckConstraint, Identity, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Ricambio(Base):

    __tablename__ = "ricambio"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    nome: Mapped[str] = mapped_column(nullable=False)
    prezzo_acquisto: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    prezzo_vendita: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    quantita_scorta: Mapped[int] = mapped_column(nullable=False)

    __table_args__ = (
        CheckConstraint(
            "quantita_scorta >= 0",
            name="check_quantita_scorta",
        ),
    )
