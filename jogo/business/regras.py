from jogo.domain.jogo import JogoController
from jogo.domain.jogador import JogadorController
from jogo.domain.partida import PartidaController
from jogo.domain.propriedade import PropriedadeController
from jogo.domain.comportamento import ComportamentoController
from jogo.domain.saldo import SaldoController
from jogo.domain.rodada import RodadaController
from jogo.domain.mercado import MercadoController

class JogoRegras():

    def __init__(self):
        # injetando controllers
        self.jc = JogoController()
        self.jgc = JogadorController()
        self.pc = PartidaController()
        self.prc = PropriedadeController()
        self.cc = ComportamentoController()
        self.sc = SaldoController()
        self.rc = RodadaController()
        self.mc = MercadoController()
    
    def criar(self, qtde_jogadores, qtde_rodadas):
        # Criando jogo
        jogo = self.jc.criar(qtde_jogadores, qtde_rodadas)
        # criando partidas
        partidas = self.pc.criar(jogo.id)
        # criando saldos dos jogadores
        for partida in partidas:
            self.sc.criar(jogo.id, partida.jogador_id, 0)
        # retorna o jogo
        return jogo
    
    # Rotina principal, executa uma iteração (rodada) de todos os jogadores
    # ou seja, anda cada jogador o número de casas sorteado nos dados e 
    # executa as regras de compra conforme o perfil de cada jogador e também
    # executa as ordens de aluguel, se for o caso, entre outros detalhes 
    # da rotina principal
    def jogar(self, jogo_id):
        saldo_inicial = 300
        saldo_rodada = 100
        n_rodada = 1
        resultado = 0
        # Pegando o total de propriedades, para não depender de número mágico
        total_propriedades = self.prc.total()
        # 1. Faça até que numero da rodada <= qtde_rodadas e que jogadores com saldo > 1
        jogo = self.jc.consultar(jogo_id)
        while jogo and n_rodada <= jogo.qtde_rodadas \
            and self.sc.consultar_qtde_com_saldo(jogo.id) > 1:
            # 1.1 Pegando o número da rodada
            n_rodada = self.rc.consultar_numero_rodada(jogo.id)
            # 2. Verifica se é primeira rodada
            if n_rodada == 1:
                # 2.1. Adiciona saldo inicial para todos jogadores
                self.pc.adicionar_saldo_inicial(jogo.id, saldo_inicial)
            # 4. Para cada jogador
            partidas = self.pc.consultar_por_jogo(jogo.id)
            for partida in partidas:
                # 4.1 Verifica se o jogador tem saldo >= 0
                conta = self.sc.consultar_por_jogador(jogo.id, partida.jogador_id)
                if conta and conta.saldo < 0:
                    # 4.1.1 Se não, elimina o jogador e vende suas propriedades e continua
                    self.pc.eliminar_jogador(jogo.id, partida.jogador_id, 1)
                    continue
                # 4.2 Joga o dado
                resultado = self.jc.jogar()
                # 4.3 Soma a posicao atual com o numero do dado e anda as casas
                casa_nova = partida.posicao_atual + resultado
                # 4.4 Verifica se jogador percorreu todas casas e reiniciou a contagem
                if casa_nova > total_propriedades:
                    # 4.4.1 Se sim, adiciona saldo de 100
                    self.sc.adicionar(jogo_id, partida.jogador_id, saldo_rodada)
                    casa_nova -= total_propriedades
                # 4.4.2 Registra a posicao atual
                self.pc.registrar_posicao_atual(jogo.id, partida.jogador_id, casa_nova)
                # 4.5 Verifica se a propriedade da casa tem dono
                # -- Pega ultima posição de mercado daquela propriedade
                tem_dono = False
                mercado = self.mc.consultar_ultima_posicao(jogo.id, casa_nova)
                if mercado:
                    # 4.5.1 Se sim, paga aluguel
                    propriedade = self.prc.consultar(mercado.propriedade_id)
                    if mercado.proprietario_id:
                        tem_dono = True
                        # se propriedade for do jogador não cobra aluguel
                        if mercado.proprietario_id != partida.jogador_id:
                            # Retira dinheiro do jogador atual
                            self.sc.retirar(jogo.id, partida.jogador_id, propriedade.valor_aluguel)
                            # Deposita na conta do proprietário
                            self.sc.adicionar(jogo.id, mercado.proprietario_id, propriedade.valor_aluguel)
                            # registra movimentação imobiliária no mercado de aluguel
                            self.mc.alugar(jogo.id, propriedade.id, mercado.proprietario_id)
                # 4.5.1 Se não, verifica perfil do comprador e efetua a compra se for o caso
                if not tem_dono:
                    propriedade = self.prc.consultar_por_posicao(casa_nova)
                    if propriedade:
                        if self.jc.calcular_comportamento(
                            partida.jogador_id, propriedade.valor_venda, 
                            propriedade.valor_aluguel, conta.saldo):
                            # se o resultado foi positivo, compra!
                            self.sc.retirar(jogo.id, partida.jogador_id, propriedade.valor_venda)
                            # efetua o registro de compra
                            self.mc.comprar(jogo.id, propriedade.id, partida.jogador_id)
        # Saiu do while
        # 5. Determina se houve vencedor ou se foi timeout
        # termina jogo e registra data e hora de termino e vencedor
        self.jc.verificar_vencedor(jogo_id, n_rodada)

    def resultado(self, jogo_id):
        return self.jc.consultar(jogo_id)