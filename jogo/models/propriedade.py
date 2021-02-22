from sqlalchemy import Column, Integer, String, Float
from jogo.dao.database import Base
from .comportamento import Comportamento

class Propriedade(Base):
    __tablename__ = 'propriedade'
    
    id = Column(Integer, primary_key=True)
    descricao = Column(String(100), nullable=True)
    valor_venda = Column(Float, nullable=False)
    valor_aluguel = Column(Float, nullable=False)
    ordem = Column(Integer, nullable=False)

    def __init__(self, descricao, valor_venda, valor_aluguel, ordem):
        self.descricao = descricao
        self.valor_venda = valor_venda
        self.valor_aluguel = valor_aluguel
        self.ordem = ordem

    def __repr__(self):
        return '<Propriedade %r>' % self.valor_venda

