import datetime
from jogo.dao.database import Database, Session
from jogo.models.propriedade import Propriedade

class PropriedadeController(Database):

    def __init__(self):
        super().__init__()

    def criar(self, descricao, valor_venda, valor_aluguel, ordem):
        obj = Propriedade(descricao, valor_venda, valor_aluguel, ordem)
        self.session.add(obj)
        self.session.commit()
        return obj
    
    def consultar(self, id):
        return self.session.query(Propriedade).filter(Propriedade.id == id).first()
    
    def consultar_por_posicao(self, posicao):
        return self.session.query(Propriedade).filter(Propriedade.ordem == posicao).first()
    
    def total(self):
        return self.session.query(Propriedade).count()
