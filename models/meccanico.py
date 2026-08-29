from sqlalchemy import Identity
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Meccanico(Base):

    __tablename__ = "meccanico"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    nome: Mapped[str] = mapped_column(nullable=False)
    specializzazione: Mapped[str | None] = mapped_column()
