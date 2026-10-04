from sqlalchemy import create_engine, String
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column

engine = create_engine('sqlite:///banco.db', echo=True)
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

class Cliente(Base):
    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(primary_key=True)
    cpf: Mapped[str] = mapped_column(String(11))
    nome: Mapped[str] = mapped_column(String(100))
    telefone: Mapped[str] = mapped_column(String(11))
    email: Mapped[str] = mapped_column(String(100))
    cep: Mapped[str] = mapped_column(String(8))

Base.metadata.create_all(engine)