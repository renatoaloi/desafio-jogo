import unittest
from desafio_bi.models.jogo import Jogo

class TestModels(unittest.TestCase):

    def test_jogo(self):
        self.assertIsInstance(Jogo(), Jogo)

if __name__ == '__main__':
    unittest.main()


# Tentando instanciar objetos

# class InitTest():
#     jogo = Jogo()
#     jogador = Jogador()
#     partida = Partida()
#     rodada = Rodada()
#     propriedade = Propriedade()
#     mercado = Mercado()
#     operacao = Operacao()
#     conta = Conta()
#     dado = Dado()
#     comportamento = Comportamento()