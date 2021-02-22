from sqlalchemy import Column, Integer, ForeignKey
from jogo.dao.database import Base
from .comportamento import Comportamento

class Rodada(Base):
    __tablename__ = 'rodada'

    id = Column(Integer, primary_key=True)
    jogo_id = Column(Integer, ForeignKey('jogo.id'), nullable=False)
    numero = Column(Integer, nullable=False)

    def __init__(self, jogo_id, numero):
        self.jogo_id = jogo_id
        self.numero = numero

    def __repr__(self):
        return '<Rodada %r>' % self.posicao_atual

