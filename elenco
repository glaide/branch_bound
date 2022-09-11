#!/usr/bin/python3
import sys
import time


OPT = sys.maxsize
X_OPT = []
ATORES = []
L_GRUPOS = 0  # num de grupos
M_ATORES = 0  # num de atores
N_PERSONAGENS = 0  # num de personagens

# argumentos:
LIMITANTE_DADA = False  # usar função limitante dos profs.
C_VIABILIDADE = True  # cortes de viabilidade
C_OTIMALIDADE = True  # cortes de otimalidade


class Ator:
    def __init__(self, valor, grupos, id):
        self.valor = valor
        self.grupos = grupos
        self.id = id

    def __repr__(self):
        return str(self.id)

    def __str__(self):
        return str(self.id)


def main():
    global ATORES
    global OPT
    global X_OPT

    leitura()
    a_escolhidos = []

    time_start = time.time()
    if not LIMITANTE_DADA:
        ATORES.sort(key=lambda x: x.valor)

    # atores.sort(key=lambda x: x.valor)

    busca_elenco_bb(a_escolhidos, ATORES)
    time_end = time.time()

    if len(X_OPT) != 0:
        X_OPT.sort(key=lambda x: x.id)
        print(" ".join(str(x) for x in X_OPT))
        print(OPT)
    else:
        print("Inviável")

    print(str(time_end - time_start), file=sys.stderr)


def leitura():
    # obtém entrada em formato de lista (um item para cada linha)
    entrada = sys.stdin.readlines()
    # retira os \n de cada linha de entrada
    for i, linha in enumerate(entrada):
        entrada[i] = linha.replace("\n", "")

    linha = entrada[0].split(" ")
    global L_GRUPOS
    global M_ATORES
    global N_PERSONAGENS
    global ATORES
    L_GRUPOS = int(linha[0])  # num de grupos
    M_ATORES = int(linha[1])  # num de atores
    N_PERSONAGENS = int(linha[2])  # num de personagens
    n_linha = 1

    # lê informação de cada ator
    for i in range(M_ATORES):
        linha = entrada[n_linha].split(" ")
        a_valor = int(linha[0])

        a_s = int(linha[1])
        grupos = []
        n_linha += 1

        for j in range(a_s):
            grupos.append(int(entrada[n_linha]))
            n_linha += 1

        ATORES.append(Ator(a_valor, grupos, i + 1))


# função limitante que o prof deu
def limitanteDada(a_escolhidos, f_faltam):
    global N_PERSONAGENS
    total = 0
    # faz o somatório
    for ator in a_escolhidos:
        total += ator.valor

    total += (N_PERSONAGENS - len(a_escolhidos)) * menor(f_faltam)
    return total


def limitanteAluna(a_escolhidos, f_faltam):
    global N_PERSONAGENS  # num de personagens
    size_e = len(a_escolhidos)
    size_f = len(f_faltam)
    # o array de atores faltando está ordenado por menor valor por número de
    # grupos que o ator satisfaz
    total = 0
    for ator in a_escolhidos:
        total += ator.valor

    i = 0
    while size_e < N_PERSONAGENS and i < size_f:
        total += f_faltam[i].valor
        size_e += 1
        i += 1

    return total


# calculando o valor mínimo de um ator numa lista de atores
def menor(atores):
    n_atores = len(atores)
    if n_atores == 0:
        return 0
    # assume como mais barato o primeiro do array
    minimo = atores[0].valor
    for i in range(1, n_atores):
        if atores[i].valor < minimo:
            minimo = atores[i].valor
    return minimo


def solucao_viavel(a_escolhidos):
    global L_GRUPOS
    global N_PERSONAGENS
    # verifica se o num de atores escolhidos está correto
    if len(a_escolhidos) != N_PERSONAGENS:
        return (False, 0)
    # verifica se todos os grupos estão representados
    grupos = dict()
    valor = 0
    for ator in a_escolhidos:
        valor += ator.valor
        for n_grupo in ator.grupos:
            grupos[n_grupo] = 1

    if len(grupos) < L_GRUPOS:
        return (False, 0)

    return (True, valor)


def busca_elenco_bb(a_escolhidos, f_faltam):
    global OPT  # sol. ótima
    global X_OPT  # val. sol. ótima
    global LIMITANTE_DADA  # usar função limitante dos profs.
    global C_VIABILIDADE  # cortes de viabilidade
    global C_OTIMALIDADE  # cortes de otimalidade

    # verifica se o grupo de atores escolhidos é viável
    (viavel, novo_val) = solucao_viavel(a_escolhidos)
    if viavel:
        if novo_val < OPT:
            OPT = novo_val
            X_OPT = a_escolhidos
    # não tem mais atores para escolher
    if len(f_faltam) == 0:
        return
    # faz o corte de viabilidade (as escolhas de atores restantes formam uma resposta possível?)
    if C_VIABILIDADE:
        if corte_viabilidade(a_escolhidos, f_faltam):
            return
    # faz o corte de otimalidade (existe a possibilidade uma escolha de atores mais barata?)
    if C_OTIMALIDADE:
        B = OPT
        if LIMITANTE_DADA:
            B = limitanteDada(a_escolhidos, f_faltam)
        else:
            B = limitanteAluna(a_escolhidos, f_faltam)
        if B >= OPT:
            return

    # ainda falta escolher atores
    E = a_escolhidos.copy()
    F = f_faltam.copy()
    ator = F.pop(0)
    # decido não escolher o próximo ator
    busca_elenco_bb(E, F)
    # decido escolher o próximo ator
    E.append(ator)
    busca_elenco_bb(E, F)


def corte_viabilidade(a_escolhidos, f_faltam):
    global L_GRUPOS  # num de grupos
    global N_PERSONAGENS  # num. personagens

    if len(f_faltam) + len(a_escolhidos) < N_PERSONAGENS:
        return True  # se for menos que precisamos, corta
    # verifica se o número de grupos (distintos) dos personagens escolhidos + o número de
    # grupos dos atores restantes (que não foram escolhidos) satisfaz o valor mínimo
    grupos = dict()
    for ator in a_escolhidos:
        for n_grupo in ator.grupos:
            grupos[n_grupo] = 1

    for ator in f_faltam:
        for n_grupo in ator.grupos:
            grupos[n_grupo] = 1

    if len(grupos) < L_GRUPOS:
        return True

    return False


if __name__ == "__main__":
    for arg in sys.argv:
        if arg == "-a":
            LIMITANTE_DADA = True
        if arg == "-f":
            C_VIABILIDADE = False
        if arg == "-o":
            C_OTIMALIDADE = False
    main()
