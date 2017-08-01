import json
from urllib import request
from pymongo import MongoClient
from model import Clube, AtletasPontos

url_mercado = "https://api.cartolafc.globo.com/mercado/status"
url_atletas = "https://api.cartolafc.globo.com/atletas/mercado"
url_rodada = "https://api.cartolafc.globo.com/partidas/"

def main():
    rodada_atual = get_rodada_atual()

    client = MongoClient('localhost', 27017)
    db = client['cartola']

    mercado = json.load(request.urlopen(url_atletas))
    calcular_pontuacao_atletas(rodada_atual-1, mercado['atletas'])

    atletas_provaveis = list(find_atletas_pontuacoes(mercado))
    clubes = computar_partidas_todas_rodadas_clubes(rodada_atual-1)

    salvar_dados(db, find_partidas(rodada_atual), atletas_provaveis, clubes)
    client.close()

def get_rodada_atual():
    mercado = json.load(request.urlopen(url_mercado))
    return mercado['rodada_atual']

def find_partidas(rodada):
    partidas = json.load(request.urlopen(url_rodada+str(rodada)))
    campos_invalidos = (set(['aproveitamento_mandante', 'aproveitamento_visitante', 'partida_data', 'local',
                             'url_confronto', 'url_transmissao']))
    partidas = map(lambda partida : filtrar_campos(partida, campos_invalidos), partidas['partidas'])
    return partidas

def find_atletas_pontuacoes(mercado):
    campos_invalidos = set(['nome', 'foto', 'variacao_num', 'scout', 'status_id', 'pontos_num'])
    atletas_validos = list(filter(lambda atleta: atleta['status_id']==7, mercado['atletas']))
    atletas_validos = adicionar_clubes(atletas_validos, mercado['clubes'])
    atletas_validos = map(lambda atleta : filtrar_campos(atleta, campos_invalidos), atletas_validos)
    return atletas_validos

def adicionar_clubes(atletas_validos, clubes):
    for atleta in atletas_validos:
        clube_id = atleta['clube_id']
        atleta['clube_nome'] = clubes[str(clube_id)]['nome']
        atleta['ultima_rodada'] = atleta['pontos_num']
    return atletas_validos

def calcular_pontuacao_atletas(ultima_rodada, atletas):
    for atleta in atletas:
        ultima_pontuacao = atleta['pontos_num']
        if ultima_pontuacao == 0:
            continue
        atletaPontos = AtletasPontos.get(atleta['atleta_id'])
        atletaPontos.add_pontuacao(str(ultima_rodada), ultima_pontuacao)
        atletaPontos.save()

def filtrar_campos(linha, campos_invalidos):
    for campo in campos_invalidos:
        del linha[campo]
    return linha

def computar_partidas_todas_rodadas_clubes(rodada_atual):
    clubes = {}
    while rodada_atual > 0:
        if check_foi_computada(clubes, rodada_atual):
            break
        for partida in find_partidas(rodada_atual):
            if partida['valida'] is True:
                clubes = computar_partida(rodada_atual, clubes, partida)
        rodada_atual -= 1
    return clubes

def computar_partida(rodada, clubes, partida):
    clube_casa = get_clube(clubes, partida['clube_casa_id'])
    clube_casa.computar_partida(partida, 'MANDANTE')
    clube_casa.computados.append(rodada)
    clubes[clube_casa._id] = clube_casa

    clube_visitante = get_clube(clubes, partida['clube_visitante_id'])
    clube_visitante.computar_partida(partida, 'VISITANTE')
    clube_visitante.computados.append(rodada)
    clubes[clube_visitante._id] = clube_visitante
    return clubes


def get_clube(clubes, clube_id):
    if clube_id in clubes:
        return clubes[clube_id]
    else:
        return Clube(_id=clube_id)

def check_foi_computada(clubes, rodada):
    if len(clubes) == 0:
        return False
    if rodada in list(clubes.values())[0].computados:
        return True
    else:
        return False

def salvar_dados(db, partidas, atletas, clubes):
    db.partidas_rodada.delete_many({})
    db.partidas_rodada.insert_many(list(partidas))
    db.atletas_rodada.delete_many({})
    db.atletas_rodada.insert_many(atletas)
    for clube in clubes.values():
        clube.save()

if __name__ == "__main__":
    main()
