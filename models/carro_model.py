from sqlalchemy import Column, Integer, String, Numeric

from shared.database import Base

# Modelo de tabela para o banco de dados
class Carros(Base):
    __tablename__ = 'carros'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(30))
    ano = Column(Integer)
    modelo = Column(String(30))
