from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Pagamento(Base):
    __tablename__ = "pagamentos"

    id = Column(Integer, primary_key=True, index=True)
    carteira_destino = Column(String, index=True)
    moeda = Column(String, index=True)
    valor = Column(Float)
    descricao = Column(String, nullable=True)
