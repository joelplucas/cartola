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

    @classmethod
    def get(cls, atleta_id):
        try:
            return cls.objects.get(_id=atleta_id)
        except DoesNotExist:
            return cls(_id=atleta_id)

class Clube(Document):
    _id = IntField(required=True, primary_key=True)
    computados = ListField(field=IntField(), required=True)
    gols_pro_mandante = IntField(required=True, default=0)
    gols_pro_visitante = IntField(required=True, default=0)
    gols_sofridos_mandante = IntField(required=True, default=0)
    gols_sofridos_visitante = IntField(required=True, default=0)

    def computar_partida(self, partida, mando_campo):
        if mando_campo is 'VISITANTE':
            self.add_partida_visitante(partida)
        elif mando_campo is 'MANDANTE':
            self.add_partida_mandante(partida)

    def add_partida_visitante(self, partida):
        self.gols_pro_visitante += partida['placar_oficial_visitante']
        self.gols_sofridos_visitante += partida['placar_oficial_mandante']

    def add_partida_mandante(self, partida):
        self.gols_pro_mandante += partida['placar_oficial_mandante']
        self.gols_sofridos_mandante += partida['placar_oficial_visitante']
