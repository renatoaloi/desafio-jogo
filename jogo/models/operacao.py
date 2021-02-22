from sqlalchemy import Column, Integer, String
from jogo.dao.database import Base

class Operacao(Base):
    __tablename__ = 'operacao'

    id = Column(Integer, primary_key=True)
    descricao = Column(String(100), unique=True, nullable=False)

    def __init__(self, descricao):
        self.descricao = descricao

    def __repr__(self):
        return '<Operacao %s>' % self.descricao

