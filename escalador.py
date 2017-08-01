class Recommender:
    def __init__(self, cartoletas_max, num_lat, num_zag, num_med, num_ata):
        self.cartoletas = 0
        self.cartoletas_max = cartoletas_max
        self.escalacao_goleiro = Escalacao_Posicao(1, 1)
        self.escalacao_laterais = Escalacao_Posicao(2, int(num_lat))
        self.escalacao_zagueiros = Escalacao_Posicao(3, int(num_zag))
        self.escalacao_meias = Escalacao_Posicao(4, int(num_med))
        self.escalacao_atacantes = Escalacao_Posicao(5, int(num_ata))
        self.escalacao_tecnico = Escalacao_Posicao(6, 1)

    def melhor_time_possivel(self, goleiros, laterais, zagueiros, meias, atacantes, tecnicos):
        self.adicionar_atletas_posicao(goleiros, self.escalacao_goleiro)
        self.adicionar_atletas_posicao(laterais, self.escalacao_laterais)
        self.adicionar_atletas_posicao(zagueiros, self.escalacao_zagueiros)
        self.adicionar_atletas_posicao(meias, self.escalacao_meias)
        self.adicionar_atletas_posicao(atacantes, self.escalacao_atacantes)
        self.adicionar_atletas_posicao(tecnicos, self.escalacao_tecnico)

    def adicionar_atletas_posicao(self, atletas, escalacao_atletas):
        while len(escalacao_atletas.escalados) < escalacao_atletas.max:
            escalacao_atletas.adicionar_atleta(atletas.index[0], atletas.iloc[0]['preco_num'])
            self.cartoletas += atletas.iloc[0]['preco_num']
            atletas.drop(atletas.index[0], inplace=True)

    def escalar_limitando_preco(self, goleiros, laterais, zagueiros, meias, atacantes, tecnicos):
        while self.cartoletas > self.cartoletas_max:
            if self.substituir_atleta(goleiros, self.escalacao_goleiro) <= self.cartoletas_max:
                break
            if len(self.escalacao_laterais.escalados)>0 and self.limitar_preco(laterais, self.escalacao_laterais):
                break
            if self.limitar_preco(zagueiros, self.escalacao_zagueiros):
                break
            if self.limitar_preco(meias, self.escalacao_meias):
                break
            if self.limitar_preco(atacantes, self.escalacao_atacantes):
                break
            if self.substituir_atleta(tecnicos, self.escalacao_tecnico) <= self.cartoletas_max:
                break

    def limitar_preco(self, atletas, escalacao_atletas):
        bateu_min = False
        for i in range(escalacao_atletas.max):
            if self.substituir_atleta(atletas, escalacao_atletas) <= self.cartoletas_max:
                bateu_min = True
                break
        return bateu_min

    def substituir_atleta(self, atletas, escalacao_atletas):
        cartoletas_removidas = escalacao_atletas.adicionar_atleta(atletas.index[0], atletas.iloc[0]['preco_num'])
        self.cartoletas -= cartoletas_removidas
        self.cartoletas += atletas.iloc[0]['preco_num']
        atletas.drop(atletas.index[0], inplace=True)
        return self.cartoletas

    def imprimir_escalacao(self, atletas_collection):
        self.escalacao_goleiro.imprimir_atletas(atletas_collection)
        self.escalacao_laterais.imprimir_atletas(atletas_collection)
        self.escalacao_zagueiros.imprimir_atletas(atletas_collection)
        self.escalacao_meias.imprimir_atletas(atletas_collection)
        self.escalacao_atacantes.imprimir_atletas(atletas_collection)
        self.escalacao_tecnico.imprimir_atletas(atletas_collection)

class Escalacao_Posicao:
    def __init__(self, posicao_id, max):
        self.posicao_id = posicao_id
        self.max = max
        self.escalados = {}

    def adicionar_atleta(self, atleta_id, preco):
        if len(self.escalados) < self.max:
            self.escalados[int(atleta_id)] = preco
            mais_caro = preco
        else:
            mais_caro = self.remover_mais_caro()
            self.escalados[int(atleta_id)] = preco
        return mais_caro

    def remover_mais_caro(self):
        mais_caro = 0
        precos_ordenados = sorted(self.escalados.values(), reverse=True)
        for key, value in self.escalados.items():
            if value == precos_ordenados[0]:
                self.escalados.pop(key)
                mais_caro = value
                break
        return mais_caro

    def imprimir_atletas(self, atletas_collection):
        atletas = atletas_collection.find({"atleta_id": {"$in": list(self.escalados)}})
        for atleta in atletas:
            print (str(atleta['atleta_id'])+" = "+atleta['apelido']+
                   " - "+atleta['clube_nome']+u" $"+str(atleta['preco_num']))