import unittest
import datetime

from jogo.domain.jogo import JogoController
from jogo.domain.jogador import JogadorController
from jogo.domain.comportamento import ComportamentoController
from jogo.domain.partida import PartidaController
from jogo.domain.rodada import RodadaController
from jogo.domain.propriedade import PropriedadeController
from jogo.domain.operacao import OperacaoController
from jogo.domain.mercado import MercadoController
from jogo.domain.saldo import SaldoController


class TestControllers(unittest.TestCase):

    def test_comportamento(self):
        c = ComportamentoController()
        obj = c.criar('teste3')
        obj = c.consultar(obj.id)
        self.assertEqual(obj.descricao, 'teste3')


if __name__ == '__main__':
    unittest.main()