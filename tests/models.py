import sys
import unittest
import datetime
from jogo.models.jogo import Jogo
from jogo.models.jogador import Jogador
from jogo.models.comportamento import Comportamento
from jogo.models.partida import Partida
from jogo.models.rodada import Rodada
from jogo.models.propriedade import Propriedade
from jogo.models.operacao import Operacao
from jogo.models.mercado import Mercado
from jogo.models.conta import Conta


class TestModels(unittest.TestCase):

    def test_jogo(self):
        obj = Jogo(datetime.datetime.now(), 1000, 4)
        self.assertIsInstance(obj, Jogo)
    
    def test_comportamento(self):
        obj = Comportamento('teste')
        self.assertIsInstance(obj, Comportamento)
    
    def test_jogador(self):
        obj_aux1 = Comportamento('teste')
        obj = Jogador(obj_aux1.id)
        self.assertIsInstance(obj, Jogador)
    
    def test_partida(self):
        obj_aux1 = Comportamento('teste2')
        obj_aux2 = Jogador(obj_aux1.id)
        obj_aux3 = Jogo(datetime.datetime.now(), 1000, 4)
        obj = Partida(obj_aux3.id, obj_aux2.id, 1)
        self.assertIsInstance(obj, Partida)
    
    def test_rodada(self):
        obj_aux1 = Jogo(datetime.datetime.now(), 1000, 4)
        obj = Rodada(obj_aux1.id, 1)
        self.assertIsInstance(obj, Rodada)
    
    def test_propriedade(self):
        obj = Propriedade('AV. TESTE', 100, 10, 1)
        self.assertIsInstance(obj, Propriedade)
    
    def test_operacao(self):
        obj = Operacao('testar')
        self.assertIsInstance(obj, Operacao)
    
    def test_mercado(self):
        obj_aux1 = Comportamento('teste2')
        obj_aux2 = Jogador(obj_aux1.id)
        obj_aux3 = Jogo(datetime.datetime.now(), 1000, 4)
        obj_aux4 = Propriedade('AV. TESTE 2', 100, 10, 1)
        obj_aux5 = Operacao('testar mais')
        obj = Mercado(obj_aux3.id, obj_aux4.id, obj_aux2.id, obj_aux5.id, 1)
        self.assertIsInstance(obj, Mercado)
    
    def test_conta(self):
        obj_aux1 = Jogador(obj_aux1.id)
        obj_aux2 = Jogo(datetime.datetime.now(), 1000, 4)
        obj = Conta(obj_aux2.id, obj_aux1.id, 100)
        self.assertIsInstance(obj, Conta)


if __name__ == '__main__':
    unittest.main()
