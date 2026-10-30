from sqlalchemy import create_engine, String, select
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column

from pathlib import Path

BASE_DIR=Path(__file__).resolve().parent
DB_PATH=BASE_DIR/"banco.db"

engine = create_engine("sqlite:///" + str(DB_PATH), echo=True)
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

cliente = Cliente(
    cpf="12345678901",
    nome="João da Silva",
    telefone="21999999999",
    email="joao@email.com",
    cep="20040002"
)

def buscar_cliente_por_cpf(cpf):

    session = SessionLocal()

    try:
        stmt = select(Cliente).where(Cliente.cpf == cpf)
        resultado = session.execute(stmt)
        cliente = resultado.scalar_one_or_none()

        return cliente
        
    finally:
        session.close()

# cliente = buscar_cliente_por_cpf("12345678901")

# if cliente:
#     print(cliente.nome)
# else:
#     print("Cliente não encontrado")

def listar_clientes():

    session = SessionLocal()

    try:
        stmt = select(Cliente)
        resultado = session.execute(stmt)
        cliente = resultado.scalars().all()

        return cliente
            
    finally:
        session.close()


