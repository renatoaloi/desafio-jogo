from sqlalchemy import Column, Integer, ForeignKey
from jogo.dao.database import Base
from .comportamento import Comportamento

class Mercado(Base):
    __tablename__ = 'mercado'

    id = Column(Integer, primary_key=True)
    jogo_id = Column(Integer, ForeignKey('jogo.id'), nullable=False)
    propriedade_id = Column(Integer, ForeignKey('propriedade.id'), nullable=False)
    proprietario_id = Column(Integer, ForeignKey('jogador.id'), nullable=True)
    operacao_id = Column(Integer, ForeignKey('operacao.id'), nullable=True)
    numero = Column(Integer, nullable=False)

    def __init__(self, jogo_id, propriedade_id, proprietario_id, operacao_id, numero):
        self.jogo_id = jogo_id
        self.propriedade_id = propriedade_id
        self.proprietario_id = proprietario_id
        self.operacao_id = operacao_id
        self.numero = numero

    def __repr__(self):
        return '<Mercado %r>' % self.numero

