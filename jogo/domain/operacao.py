import datetime
from jogo.dao.database import Database, Session
from jogo.models.operacao import Operacao

class OperacaoController(Database):

    def __init__(self):
        super().__init__()

    def criar(self, descricao):
        obj = Operacao(descricao)
        self.session.add(obj)
        self.session.commit()
        return obj
    
    def consultar(self, id):
        return self.session.query(Operacao).filter(Operacao.id == id).first()
