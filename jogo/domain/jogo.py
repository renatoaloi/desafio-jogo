import datetime

from jogo.dao.database import Database, Session
from jogo.util import generate_random

from jogo.models.jogo import Jogo
from jogo.models.comportamento import Comportamento
from jogo.models.jogador import Jogador
from jogo.models.propriedade import Propriedade
from jogo.models.operacao import Operacao

from jogo.domain.jogador import JogadorController
from jogo.domain.propriedade import PropriedadeController
from jogo.domain.comportamento import ComportamentoController
from jogo.domain.operacao import OperacaoController
from jogo.domain.partida import PartidaController
from jogo.domain.saldo import SaldoController


class JogoController(Database):

    def __init__(self):
        super().__init__()
        # injetando controllers
        self.jgc = JogadorController()
        self.prc = PropriedadeController()
        self.cc = ComportamentoController()
        self.oc = OperacaoController()
        self.pc = PartidaController()
        self.sc = SaldoController()
        # iniciando tabelas e dados auxiliares
        self.init_tabelas()

    def criar(self, qtde_jogadores, qtde_rodadas):
        self.session = Session()
        dt_ini = datetime.datetime.now()
        jogo = Jogo(dt_ini, qtde_rodadas, qtde_jogadores)
        self.session.add(jogo)
        self.session.commit()
        return jogo
    
    def jogar(self):
        return generate_random([], 6)
    
    def consultar(self, id):
        return self.session.query(Jogo).filter(Jogo.id==id).first()
    
    def calcular_comportamento(self, jogador_id, valor, aluguel, saldo):
        jogador = self.jgc.consultar(jogador_id)
        if jogador:
            perfil = self.cc.consultar(jogador.comportamento_id)
            if perfil.descricao == 'impulsivo' and valor <= saldo:
                return True
            elif perfil.descricao == 'exigente' and valor <= saldo and aluguel > 50.0: 
                return True
            elif perfil.descricao == 'cauteloso' and valor <= saldo - 80:
                return True
            elif perfil.descricao == 'aleatório' and valor <= saldo:
                #random de 50%
                numero = generate_random([], 2)
                return numero == 1
            else:
                return False
        return False
    
    def verificar_vencedor(self, jogo_id, n_rodada):
        partidas = self.pc.consultar_por_jogo(jogo_id)
        saldo_maior = 0
        vencedor = 0
        ordem = 0
        for partida in partidas:
            conta = self.sc.consultar_por_jogador(jogo_id, partida.jogador_id)
            if conta.saldo >= saldo_maior:
                if conta.saldo == saldo_maior:
                    # desempate pela ordem
                    if partida.ordem < ordem:
                        vencedor = partida.jogador_id
                else: 
                    vencedor = partida.jogador_id
                saldo_maior = conta.saldo
                ordem = partida.ordem
        # finalizando o jogo
        jogo = self.consultar(jogo_id)
        jogo.data_fim = datetime.datetime.now()
        jogo.vencedor_id = vencedor
        jogo.rodadas = n_rodada
        self.session.commit()
    
    def init_tabelas(self):
        # Criando operações
        operacoes = self.session.query(Operacao).first()
        ops = [
                'comprar',
                'vender',
                'alugar'
            ]
        if not operacoes:
            for op in ops:
                self.oc.criar(op)

        # Criando comportamentos
        comportamentos = self.session.query(Comportamento).first()
        comps = [
                'impulsivo',
                'exigente',
                'cauteloso',
                'aleatório'
            ]
        if not comportamentos:
            for comp in comps:
                self.cc.criar(comp)

        # Criando jogadores
        jogadores = self.session.query(Jogador).first()
        if not jogadores:
            for comp in comps:
                comportamento = self.session.query(Comportamento).filter(Comportamento.descricao == comp).first()
                if comportamento:
                    self.jgc.criar(comportamento.id)
        
        # Criando propriedades
        propriedades = self.session.query(Propriedade).first()
        if not propriedades:
            props = [
                Propriedade("AV. NIEMEYER", 100, 10, 1),
                Propriedade("AV. BEIRA MAR", 160, 16, 2),
                Propriedade("AV. IBIRAPUERA", 220, 28, 3),
                Propriedade("PRAÇA DA SÉ", 250, 24, 4),
                Propriedade("RUA DA CONSOLAÇÃO", 280, 24, 5),
                Propriedade("AV. JUSCELINO KUBITSCHEK", 240, 38, 6),
                Propriedade("RUA OSCAR FREIRE", 220, 51, 7),
                Propriedade("VIADUTO DO CHÁ", 280, 26, 8),
                Propriedade("HIGIENÓPOLIS", 600, 65, 9),
                Propriedade("JARDINS", 450, 58, 10),
                Propriedade("AV. SÃO JOÃO", 220, 38, 11),
                Propriedade("PONTE DO GUAÍBA", 240, 30, 12),
                Propriedade("AV. PAULISTA", 260, 32, 13),
                Propriedade("AV. RECIFE", 240, 32, 14),
                Propriedade("AV. IPIRANGA", 200, 36, 15),
                Propriedade("PRAÇA DOS TRÊS PODERES", 420, 51, 16),
                Propriedade("AV. DO CONTORNO", 400, 56, 17),
                Propriedade("BARRA DA TIJUCA", 360, 32, 18),
                Propriedade("PONTE RIO-NITERÓI", 280, 32, 19),
                Propriedade("MARINA DA GLÓRIA", 260, 36, 20)
            ]
            for prop in props:
                self.prc.criar(prop.descricao, prop.valor_venda, prop.valor_aluguel, prop.ordem)