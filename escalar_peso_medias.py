from sys import argv
import pandas as pd
from pymongo import DESCENDING, MongoClient
from escalador import Escalador

def main(argv):
    min_rodadas = 4

    client = MongoClient('localhost', 27017)
    db = client['cartola']
    atletas_collection = db.atletas_rodada
    partidas = list(db.partidas_rodada.find())

    times_validos = list(times_em_casa(partidas).union(times_visitantes_primeiros(partidas)))
    #times_validos = list(todos_times(partidas))
    goleiros = carregar_atletas_melhores_medias(1, min_rodadas, times_validos, atletas_collection)
    laterais = carregar_atletas_melhores_medias(2, min_rodadas, times_validos, atletas_collection)
    zagueiros = carregar_atletas_melhores_medias(3, min_rodadas, times_validos, atletas_collection)
    meias = carregar_atletas_melhores_medias(4, min_rodadas, times_validos, atletas_collection)
    atacantes = carregar_atletas_melhores_medias(5, min_rodadas, times_validos, atletas_collection)
    tecnicos = carregar_atletas_melhores_medias(6, min_rodadas, times_validos, atletas_collection)

    recommender = Escalador(goleiros, laterais, zagueiros, meias, atacantes, tecnicos)
    recommender.melhor_time_possivel(argv[3], float(argv[4]), argv[5], argv[6], argv[7], argv[8])
    recommender.escalar_limitando_preco(atletas_collection, argv[1], argv[2])

    client.close()


def times_em_casa(partidas):
    times = set()
    [times.add(partida['clube_casa_id']) for partida in partidas]
    return times

def todos_times(partidas):
    times = set()
    [times.add(partida['clube_casa_id']) for partida in partidas]
    [times.add(partida['clube_visitante_id']) for partida in partidas]
    return times

def times_visitantes_primeiros(partidas):
    times = set()
    for partida in partidas:
        if partida['clube_visitante_posicao'] < partida['clube_casa_posicao']:
            times.add(partida['clube_visitante_id'])
    return times

def carregar_atletas_melhores_medias(posicao, min_rodadas, times, atletas_collection):
    atletas = list(atletas_collection.find({"jogos_num": {"$gte": min_rodadas}, "posicao_id": posicao, "clube_id": {"$in": times}}).sort([("media_num",DESCENDING)]))
    return pd.DataFrame(list(atletas)).set_index('atleta_id')
if __name__ == "__main__":
    main(argv)