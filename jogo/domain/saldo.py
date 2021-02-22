import datetime
from jogo.dao.database import Database, Session
from jogo.models.conta import Conta
from jogo.models.jogo import Jogo
from jogo.models.jogador import Jogador

class SaldoController(Database):

    def __init__(self):
        super().__init__()

    def criar(self, jogo_id, jogador_id, saldo):
        obj = Conta(jogo_id, jogador_id, saldo)
        self.session.add(obj)
        self.session.commit()
        return obj
    
    def consultar(self, id):
        return self.session.query(Conta).filter(Conta.id == id).first()

    def consultar_qtde_com_saldo(self, jogo_id):
        return self.session.query(Conta).filter(
            Conta.jogo_id == jogo_id).filter(
                Conta.saldo >= 0).count()
    
    def consultar_por_jogador(self, jogo_id, jogador_id):
        return self.session.query(Conta).filter(
            Conta.jogo_id == jogo_id).filter(
                Conta.jogador_id == jogador_id).first()
    
    def adicionar(self, jogo_id, jogador_id, valor):
        self._manipular_saldo(jogo_id, jogador_id, valor)
    
    def retirar(self, jogo_id, jogador_id, valor):
        self._manipular_saldo(jogo_id, jogador_id, valor, False)
    
    def _manipular_saldo(self, jogo_id, jogador_id, valor, adicao=True):
        conta = self.session.query(Conta).filter(
            Conta.jogo_id == jogo_id).filter(
                Conta.jogador_id == jogador_id).first()
        if conta:
            conta.saldo = (conta.saldo + valor) if adicao else (conta.saldo - valor)
        self.session.commit()

