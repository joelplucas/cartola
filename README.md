# CARTOLA

Roda com python3.6.1

# Scripts
## crawler
- Acessa a API do Cartola e faz a extração de dados de jogadores e partidas da rodada atual
- Salva dados no DB "cartola" do MongoDB.
- Deve ser executado pelo menos 1 vez na rodada quando o mercado estiver aberto.
- A collection "atletas_pontos" salva o histórico de pontuação para cada atleta, atualizando seu conteúdo cada vez que o crawler for executado. Futuramente (quando houverem mais dados de rodadas) será calculado o desvio padrão de cada jogador (dado não disponível na API do Cartola).
- Não há problema de executá-lo mais de uma vez, pois os dados de atetlas e partidas são sobrescritos e os dados de pontuação não são alterados caso já tenha registro do jogador na rodada atual.

## escalar_peso_medias
- Parâmetros de entrada: <email> <password> <esquema_de_jogo> <cartoletas_disponíveis> <numero_de_laterais> <numero_de_zagueiros> <numero_de_meias> <numero_de_atacantes>
- parametro <esquema_de_jogo>: verificar o código (número inteiro) em https://api.cartolafc.globo.com/esquemas
- Se <esquema_de_jogo>==0 então não autentica e não escala jogadores (para fins de teste)
- Estratégia que recomenda a escalação de jogadores. 
- Inicialmente são considerados apenas os jogadores de times que vão jogar em casa ou que estão melhores colocados que seus adversários na rodada.
- O algoritmo tenta escalar os jogadores com as maiores médias. Caso o time supere a quantidade de cartoletas disponíveis, o algoritmo  itera sucessivamente para buscar os próximos jogadores da fila. 

## escalar_peso_saldo_clube
- Mesmos parâmetros de escalar_peso_medias

## TODO
- automatizar parâmetros do esquema de jogo
- Mais estratégias (pode-se extender a classe "Escalador")
