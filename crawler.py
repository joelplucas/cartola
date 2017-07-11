import json
from urllib2 import urlopen
from pymongo import MongoClient
from model import AtletasPontos
from mongoengine import DoesNotExist

url_mercado = "https://api.cartolafc.globo.com/mercado/status"
url_atletas = "https://api.cartolafc.globo.com/atletas/mercado"
url_rodada = "https://api.cartolafc.globo.com/partidas/"

def main():
    rodada = rodada_atual()
    partidas = find_partidas(rodada)

    mercado = json.load(urlopen(url_atletas))
    client = MongoClient('localhost', 27017)
    db = client['cartola']

    calcular_pontuacoes(rodada-1, mercado['atletas'])
    atletas_provaveis = find_atletas_pontuacoes(mercado)
    salvar_dados(db, partidas, atletas_provaveis)
    client.close()

def rodada_atual():
    mercado = json.load(urlopen(url_mercado))
    return mercado['rodada_atual']

def find_partidas(rodada):
    partidas = json.load(urlopen(url_rodada+str(rodada)))
    campos_invalidos = (set(['aproveitamento_mandante', 'aproveitamento_visitante', 'partida_data', 'local', 'valida', 'placar_oficial_mandante',
                             'placar_oficial_visitante', 'placar_oficial_visitante', 'url_confronto', 'url_transmissao']))
    partidas = map(lambda partida : filtrar_campos(partida, campos_invalidos), partidas['partidas'])
    return partidas

def find_atletas_pontuacoes(mercado):
    campos_invalidos = set(['nome', 'foto', 'variacao_num', 'scout', 'status_id', 'pontos_num'])
    atletas_validos = filter(lambda atleta: atleta['status_id']==7, mercado['atletas'])
    atletas_validos = adicionar_clubes(atletas_validos, mercado['clubes'])
    atletas_validos = map(lambda atleta : filtrar_campos(atleta, campos_invalidos), atletas_validos)
    return atletas_validos

def adicionar_clubes(atletas_validos, clubes):
    for atleta in atletas_validos:
        clube_id = atleta['clube_id']
        atleta['clube_nome'] = clubes[str(clube_id)]['nome']
        atleta['ultima_rodada'] = atleta['pontos_num']
    return atletas_validos

def calcular_pontuacoes(ultima_rodada, atletas):
    for atleta in atletas:
        ultima_pontuacao = atleta['pontos_num']
        if ultima_pontuacao == 0:
            continue
        atletaPontos = get_pontuacao_atleta(atleta['atleta_id'])
        if atletaPontos is None:
            atletaPontos = AtletasPontos(_id=atleta['atleta_id'])
        atletaPontos.add_pontuacao(str(ultima_rodada), ultima_pontuacao)
        atletaPontos.save()

def get_pontuacao_atleta(atleta_id):
    try:
        return AtletasPontos.objects.get(_id=atleta_id)
    except DoesNotExist:
        return None

def filtrar_campos(linha, campos_invalidos):
    for campo in campos_invalidos:
        del linha[campo]
    return linha

def salvar_dados(db, partidas, atletas):
    db.partidas_rodada.delete_many({})
    db.partidas_rodada.insert_many(partidas)
    db.atletas_rodada.delete_many({})
    db.atletas_rodada.insert_many(atletas)

if __name__ == "__main__":
    main()
