import datetime

from sqlalchemy import desc

from jogo.dao.database import Database, Session
from jogo.models.rodada import Rodada


class RodadaController(Database):

    def __init__(self):
        super().__init__()

    def criar(self, jogo_id, numero):
        obj = Rodada(jogo_id, numero)
        self.session.add(obj)
        self.session.commit()
        return obj
    
    def consultar(self, id):
        return self.session.query(Rodada).filter(Rodada.id == id).first()

    def consultar_por_numero(self, jogo_id, numero):
        return self.session.query(Rodada).filter(
            Rodada.jogo_id == jogo_id).filter(
                Rodada.numero == numero).first()

    def consultar_numero_rodada(self, jogo_id):
        # verificando rodada anterior
        n_rodada = 1
        rodada_ant = self.session.query(Rodada).filter(
            Rodada.jogo_id == jogo_id).order_by(
                desc(Rodada.numero)).first()
        if rodada_ant:
            n_rodada = rodada_ant.numero + 1
        # registrando a rodada
        rodada = Rodada(jogo_id, n_rodada)
        self.session.add(rodada)
        self.session.commit()
        # retorna o numero da rodada anterior + 1
        return n_rodada
