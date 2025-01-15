from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Veiculo(Base):
    __tablename__ = "veiculos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    cor = Column(String)
    km = Column(Float)
    valor = Column(Float)
    ano = Column(Integer)
