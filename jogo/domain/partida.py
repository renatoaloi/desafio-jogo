import datetime

from jogo.dao.database import Database, Session
from jogo.util import generate_random

from jogo.models.partida import Partida
from jogo.models.jogo import Jogo

from jogo.domain.jogador import JogadorController
from jogo.domain.saldo import SaldoController
from jogo.domain.mercado import MercadoController


class PartidaController(Database):

    def __init__(self):
        super().__init__()

        self.jgc = JogadorController()
        self.sc = SaldoController()
        self.mc = MercadoController()

    def criar(self, jogo_id):
        # array pra verificar se ordem já foi sorteada
        sorteados = []

        # Criando partidas dos jogadores
        partidas = []
        jogo = self.session.query(Jogo).filter(Jogo.id == jogo_id).first()
        if jogo:
            for i in range(1, jogo.qtde_jogadores + 1):
                jogador = self.jgc.consultar(i)
                # cria ordem de 1 a 4 de forma aleatória
                ordem = generate_random(sorteados)
                sorteados.append(ordem)
                # criando a partida para o jogador, na ordem sorteada
                partida = Partida(jogo_id, jogador.id, ordem)
                partidas.append(partida)
        
            for partida in partidas:
                self.session.add(partida)
            self.session.commit()

        # retorna array de partidas criadas
        return partidas
    
    def consultar(self, id):
        return self.session.query(Partida).filter(Partida.id==id).first()
    
    def consultar_por_jogo(self, jogo_id):
        return self.session.query(Partida).filter(
            Partida.jogo_id == jogo_id
        ).filter(
            Partida.eliminado == False
        ).order_by(Partida.ordem)

    def adicionar_saldo_inicial(self, jogo_id, saldo):
        partidas = self.session.query(Partida).filter(Partida.jogo_id == jogo_id)
        for partida in partidas:
            self.sc.adicionar(jogo_id, partida.jogador_id, saldo)
    
    def registrar_posicao_atual(self, jogo_id, jogador_id, posicao_atual):
        partida = self.session.query(Partida).filter(
            Partida.jogo_id == jogo_id
        ).filter(
            Partida.jogador_id == jogador_id
        ).first()
        partida.posicao_atual = posicao_atual
        self.session.commit()

    def eliminar_jogador(self, jogo_id, jogador_id, operacao_id):
        jogador = self.jgc.consultar(jogador_id)
        if jogador:
            # Vendendo propriedades
            mercados = self.mc.consultar_compras_do_jogador(jogo_id, jogador_id, operacao_id)
            for mercado in mercados:
                self.mc.vender(jogo_id, mercado.propriedade_id, jogador_id)
            # Marcando jogador como eliminado
            partida = self.session.query(Partida).filter(
                Partida.jogo_id == jogo_id
            ).filter(
                Partida.jogador_id == jogador_id
            ).first()
            partida.eliminado = True
            self.session.commit()
