import datetime

from sqlalchemy import desc

from jogo.dao.database import Database, Session

from jogo.models.mercado import Mercado
from jogo.models.propriedade import Propriedade
from jogo.models.operacao import Operacao

class MercadoController(Database):

    def __init__(self):
        super().__init__()

    def criar(self, jogo_id, propriedade_id, proprietario_id, operacao_id, numero):
        obj = Mercado(jogo_id, propriedade_id, proprietario_id, operacao_id, numero)
        self.session.add(obj)
        self.session.commit()
        return obj
    
    def consultar(self, id):
        return self.session.query(Mercado).filter(Mercado.id == id).first()
    
    def consultar_compras_do_jogador(self, jogo_id, jogador_id, operacao_id):
         return self.session.query(Mercado).filter(Mercado.jogo_id == jogo_id).filter(
                Mercado.proprietario_id == jogador_id
            ).filter(Mercado.operacao_id == operacao_id)

    def consultar_ultima_posicao(self, jogo_id, posicao_atual):
        propriedade = self.session.query(Propriedade).filter(Propriedade.ordem == posicao_atual).first()
        if propriedade:
            return self.session.query(Mercado).filter(
                Mercado.propriedade_id == propriedade.id).filter(
                    Mercado.jogo_id == jogo_id).order_by(
                        desc(Mercado.numero)).first()
        return None

    def comprar(self, jogo_id, propriedade_id, proprietario_id):
        return self._operar(jogo_id, propriedade_id, proprietario_id)
    
    def vender(self, jogo_id, propriedade_id, proprietario_id):
        return self._operar(jogo_id, propriedade_id, proprietario_id, 'vender')
    
    def alugar(self, jogo_id, propriedade_id, proprietario_id):
        return self._operar(jogo_id, propriedade_id, proprietario_id, 'alugar')
    
    def _operar(self, jogo_id, propriedade_id, proprietario_id, modo='comprar'):
        propriedade = self.session.query(Propriedade).filter(Propriedade.id == propriedade_id).first()
        if propriedade:
            operacao = self.session.query(Operacao).filter(Operacao.descricao == modo).first()
            if operacao:
                numero = self._consultar_ultimo_numero(jogo_id)
                prop_id = proprietario_id
                if modo == 'vender':
                    prop_id = None
                mercado = Mercado(jogo_id, propriedade_id, prop_id, operacao.id, numero)
                self.session.add(mercado)
                self.session.commit()
                return mercado
        return None
    
    def _consultar_ultimo_numero(self, jogo_id):
        ultimo_numero = 1
        mercado = self.session.query(Mercado).filter(Mercado.jogo_id == jogo_id).order_by(desc(Mercado.numero)).first()
        if mercado:
            ultimo_numero = mercado.numero + 1
        return ultimo_numero
