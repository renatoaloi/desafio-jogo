from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from jogo.dao.database import Base
from jogo.models.jogo import Jogo

class Jogador(Base):
    __tablename__ = 'jogador'

    id = Column(Integer, primary_key=True)
    comportamento_id = Column(Integer, ForeignKey('comportamento.id'), nullable=False)
    jogos_vencedores = relationship('Jogo', backref='jogador', lazy=True)

    def __init__(self, comportamento_id):
        self.comportamento_id = comportamento_id

    def __repr__(self):
        return '<Jogador %r>' % self.comportamento_id

