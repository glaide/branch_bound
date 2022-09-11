#!/usr/bin/python3
import sys
import time
from tracemalloc import start

# variavel com o valor solucao otimo
OPT = sys.maxsize

# conjunto de atores com solucao otima
Xopt = []
atores = []
count = 0
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


def solucao_viavel(A_ESCOLHIDOS):
    """retorna(viavel: true or false, valor otimo atual)"""
    grupos = dict()
    valor = 0

    if len(A_ESCOLHIDOS) != N_PERSONAGENS:
        # se n de escolhidos nao satisfaz o numero de personagens necessarios
        return (False, 0)

    for ator in A_ESCOLHIDOS:
        # soma dos valores de atores já escolhidos
        valor += ator.valor
        # conta o numero de grupos que já foi satisfeito
        for grupo_indice in ator.grupos:
            grupos[grupo_indice] = 1

    if len(grupos) != L_GRUPOS:
        # se o numero total de grupos dos escolhidos nao for o numero total de grupos, nao é viavel
        return (False, 0)

    return (True, valor)


def corte_viabilidade(A_ESCOLHIDOS, A_FALTAM):
    """retorna true or false para fazer o corte de viabilidade"""
    grupos = dict()
    for ator in A_ESCOLHIDOS:
        # conta o numero de grupos que já foi satisfeito
        for grupo_indice in ator.grupos:
            grupos[grupo_indice] = 1

    for ator in A_FALTAM:
        # conta o numero de grupos que já foi satisfeito
        for grupo_indice in ator.grupos:
            grupos[grupo_indice] = 1

    size_E = len(A_ESCOLHIDOS)
    size_F = len(A_FALTAM)

    if (size_E + size_F) < N_PERSONAGENS:
        # se o numero de atores escolhidos+faltantes for menor que o n de personagens total, n é viavel
        return False

    if len(grupos) < L_GRUPOS:
        # se o numero de grupos já escolhidos+faltantes for menor que o n de grupos total, n é viavel
        return False

    return True


def min(A_FALTAM):
    # alterar no futuro para buscar melhorias
    faltam = A_FALTAM.copy()
    return faltam.sort()


def limitante_dada(A_ESCOLHIDOS, A_FALTAM):
    v_total = 0
    for ator in A_ESCOLHIDOS:
        v_total += ator.valor
    menor = min(A_FALTAM)
    v_total += (N_PERSONAGENS - len(A_ESCOLHIDOS)) * menor[0]
    return v_total


def limitante_alunas(A_ESCOLHIDOS, A_FALTAM):
    v_total = 0
    i = 0
    for ator in A_ESCOLHIDOS:
        v_total += ator.valor
    total_escolhidos = len(A_ESCOLHIDOS)
    total_faltam = len(A_FALTAM)

    while total_escolhidos < N_PERSONAGENS and i < total_faltam:
        v_total += A_FALTAM[i].valor
        i += 1
        total_escolhidos += 1
    return v_total


def leitura():
    """ "Lê todos os dados de entrada"""
    global L_GRUPOS
    global M_ATORES
    global N_PERSONAGENS
    # leitura dos valores iniciais
    entrada = sys.stdin.readlines()
    for i, linha in enumerate(entrada):
        entrada[i] = linha.replace("\n", "")
    linha = entrada[0].split(" ")

    L_GRUPOS = int(linha[0])  # num de grupos
    M_ATORES = int(linha[1])  # num de atores
    N_PERSONAGENS = int(linha[2])  # num de personagens
    for i in range(M_ATORES):
        linha = entrada[i + 1].split(" ")
        ator_v = int(linha[0])
        ator_s = int(linha[1])
        grupos = []
        for j in range(ator_s):
            grupos.append(j + 1)
        atores.append(Ator(ator_v, grupos, i + 1))


def main():
    """inicio com a leitura"""

    leitura()
    global A_ESCOLHIDOS
    global A_FALTAM
    A_FALTAM = []
    A_ESCOLHIDOS = []
    # se eh a funcao dos alunos, faz uma ordenacao nos valores
    start_time = time.time()

    if not LIMITANTE_DADA:
        atores.sort(key=lambda x: x.valor)
    busca_elenco(A_ESCOLHIDOS, atores)
    time_end = time.time()

    if len(Xopt):
        Xopt.sort(key=lambda x: x.id)
        print(" ".join(str(x) for x in Xopt))
        print(OPT)
    else:
        print("Inviável")

    print(str(count) + "\n" + str(time_end - start_time), file=sys.stderr)


def busca_elenco(A_ESCOLHIDOS, A_FALTAM):
    # verifica se é viavel
    (viavel, nova_solucao_otima) = solucao_viavel(A_ESCOLHIDOS)
    # se é viavel, atualiza os valores da solucao
    if viavel:
        if nova_solucao_otima < OPT:
            OPT = nova_solucao_otima
            Xopt = A_ESCOLHIDOS
    # nao tem mais atores para verificar
    if not len(atores):
        return

    # verifica se há corte de viabilidade
    if C_VIABILIDADE:
        corte_v = corte_viabilidade(A_ESCOLHIDOS, A_FALTAM)
        if corte_v:
            return
    # verifica se ja corte de otimalidade
    if C_OTIMALIDADE:
        # verifica qual é a funcao limitante
        if LIMITANTE_DADA:
            v_atual = limitante_dada(A_ESCOLHIDOS, A_FALTAM)
        else:
            v_atual = limitante_alunas(A_ESCOLHIDOS, A_FALTAM)

        if v_atual >= OPT:
            return
    # ainda falta escolher atores
    e_atores = A_ESCOLHIDOS.copy()
    f_atores = A_FALTAM.copy()
    ator = f_atores.pop(0)
    # decido não escolher o próximo ator
    busca_elenco(e_atores, f_atores)
    # decido escolher o próximo ator
    e_atores.append(ator)
    busca_elenco(e_atores, f_atores)


if __name__ == "__main__":
    for arg in sys.argv:
        if arg == "-a":
            LIMITANTE_DADA = True
        if arg == "-f":
            C_VIABILIDADE = False
        if arg == "-o":
            C_OTIMALIDADE = False
    main()
