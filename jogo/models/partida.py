from sqlalchemy import Column, Integer, Boolean, ForeignKey
from jogo.dao.database import Base
from .comportamento import Comportamento

class Partida(Base):
    __tablename__ = 'partida'

    id = Column(Integer, primary_key=True)
    jogo_id = Column(Integer, ForeignKey('jogo.id'), nullable=False)
    jogador_id = Column(Integer, ForeignKey('jogador.id'), nullable=False)
    posicao_atual = Column(Integer, nullable=False)
    ordem = Column(Integer, nullable=False)
    eliminado = Column(Boolean, nullable=False)

    def __init__(self, jogo_id, jogador_id, ordem, posicao_atual=0, eliminado=False):
        self.jogo_id = jogo_id
        self.jogador_id = jogador_id
        self.ordem = ordem
        self.posicao_atual = posicao_atual
        self.eliminado = eliminado

    def __repr__(self):
        return '<Partida %r>' % self.ordem

    @property
    def serialize(self):
        return {
            'id': self.id,
            'jogo_id': self.jogo_id,
            'jogador_id': self.jogador_id,
            'ordem': self.ordem,
            'posicao_atual': self.posicao_atual,
            'eliminado': self.eliminado
        }
