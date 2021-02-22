import datetime
from jogo.dao.database import Database, Session
from jogo.models.comportamento import Comportamento

class ComportamentoController(Database):

    def __init__(self):
        super().__init__()

    def criar(self, descricao):
        try:
            obj = Comportamento(descricao)
            self.session.add(obj)
            self.session.commit()
        except:
            self.session.rollback()
        return obj
    
    def consultar(self, id):
        return self.session.query(Comportamento).filter(Comportamento.id==id).first()
