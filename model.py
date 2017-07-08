from mongoengine import *

connect('cartola')

class AtletasPontos(Document):
    _id = IntField(required=True, primary_key=True)
    rodadas_pontos = MapField(field=FloatField())
    pontos_total = FloatField(required=True, default=0)
    num_jogos = IntField(required=True, default=0)
    media = FloatField(required=True, default=0)
    std = FloatField(required=True, default=0)

    def add_pontuacao(self, ultima_rodada, pontuacao):
        if ultima_rodada in self.rodadas_pontos:
            return
        self.pontos_total += pontuacao
        self.num_jogos += 1
        self.media = self.pontos_total / self.num_jogos
        self.rodadas_pontos[ultima_rodada] = pontuacao