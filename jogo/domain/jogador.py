import datetime
from jogo.dao.database import Database, Session
from jogo.models.jogador import Jogador

class JogadorController(Database):

    def __init__(self):
        super().__init__()

    def criar(self, comportamento_id):
        obj = Jogador(comportamento_id)
        self.session.add(obj)
        self.session.commit()
        return obj
    
    def consultar(self, id):
        return self.session.query(Jogador).filter(Jogador.id == id).first()
    

