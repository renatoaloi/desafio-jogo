from sqlalchemy import Column, Integer, DateTime, ForeignKey
from jogo.dao.database import Base

class Jogo(Base):
    __tablename__ = 'jogo'
    
    id = Column(Integer, primary_key=True)
    data_inicio = Column(DateTime, nullable=False)
    data_fim = Column(DateTime, nullable=True)
    qtde_rodadas = Column(Integer, default=0)
    qtde_jogadores = Column(Integer, default=4)
    vencedor_id = Column(Integer, ForeignKey('jogador.id'), nullable=True)
    rodadas = Column(Integer, default=0)

    def __init__(self, data_inicio, qtde_rodadas, qtde_jogadores):
        self.data_inicio = data_inicio
        self.data_fim = None
        self.qtde_rodadas = qtde_rodadas
        self.qtde_jogadores = qtde_jogadores
        self.vencedor_id = None
        self.rodadas = 0

    def __repr__(self):
        return """
            <Jogo data_inicio=%s data_fim=%s qtde_jogadores=%s qtde_rodadas=%s vencedor_id=%s rodadas=%s />
        """ % (
            self.data_inicio.strftime("%d/%m/%Y, %H:%M:%S"),
            self.data_fim.strftime("%d/%m/%Y, %H:%M:%S"),
            self.qtde_jogadores, 
            self.qtde_rodadas,
            self.vencedor_id,
            self.rodadas
        )

    @property
    def serialize(self):
        return {
            'id': self.id,
            'data_inicio': self.data_inicio.strftime("%d/%m/%Y, %H:%M:%S"),
            'data_fim': self.data_fim.strftime("%d/%m/%Y, %H:%M:%S"),
            'qtde_rodadas': self.qtde_rodadas,
            'qtde_jogadores': self.qtde_jogadores,
            'vencedor_id': self.vencedor_id,
            'rodadas': self.rodadas
        }
