from sqlalchemy import Column, Integer, String, Float, ForeignKey
from jogo.dao.database import Base

class Conta(Base):
    __tablename__ = 'conta'

    id = Column(Integer, primary_key=True)
    jogo_id = Column(Integer, ForeignKey('jogo.id'), nullable=False)
    jogador_id = Column(Integer, ForeignKey('jogador.id'), nullable=True)
    saldo = Column(Float, nullable=False)

    def __init__(self, jogo_id, jogador_id, saldo):
        self.jogo_id = jogo_id
        self.jogador_id = jogador_id
        self.saldo = saldo

    def __repr__(self):
        return '<Conta %r>' % self.saldo

