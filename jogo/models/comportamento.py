from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from jogo.dao.database import Base
from jogo.models.jogador import Jogador

class Comportamento(Base):
    __tablename__ = 'comportamento'

    id = Column(Integer, primary_key=True)
    descricao = Column(String(100), unique=True, nullable=False)
    jogadores = relationship('Jogador', backref='comportamento', lazy=True)

    def __init__(self, descricao):
        self.descricao = descricao

    def __repr__(self):
        return '<Comportamento %r>' % self.descricao

