from jogo.business.regras import JogoRegras
from threading import Thread
import requests
import json


class App():
    def __init__(self):
        # injetando controllers
        self.jr = JogoRegras()

    def criar(self):
        return self.jr.criar(4, 1000)

    def jogar(self, jogo_id):
        self.jr.jogar(jogo_id)
    
    def resultado(self, jogo_id):
        return self.jr.resultado(jogo_id)


# class Th(Thread):
#     def __init__(self):
#         Thread.__init__(self)
#         self.app = App()
    
#     def run(self):
#         jogo = self.app.criar()
#         self.app.jogar(jogo.id)
#         print(self.app.resultado(jogo.id))

def main():
    #for i in range(300):
    #    a = Th()
    #    a.start()
    app = App()
    jogo = app.criar()
    app.jogar(jogo.id)
    jogo = app.resultado(jogo.id)
    r = requests.post(
        "http://192.168.15.8:5000/jogo/resultado", 
        json=jogo.serialize
    )
    print(jogo.serialize)

if __name__ == '__main__':
    main()
