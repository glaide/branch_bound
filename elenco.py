#!/usr/bin/python3
from glob import glob
import sys
import time


# variavel com o valor solucao otimo

# conjunto de atores com solucao otima
OPT_VALOR = sys.maxsize
Xopt = []
atores = []
A_FALTAM = []
A_ESCOLHIDOS = []


# argumentos:
LIMITANTE_DADA = False  # usar função limitante dos profs.
C_VIABILIDADE = True  # cortes de viabilidade
C_OTIMALIDADE = True  # cortes de otimalidade
L_GRUPOS = 0
M_ATORES = 0
N_PERSONAGENS = 0


class Ator:
    """ator, que possui um valor, percence a grupos com os id passados"""

    def __init__(self, valor, grupos, id_a):
        self.valor = valor
        self.grupos = grupos
        self.id_a = id_a

    def __repr__(self):
        return str(self.id_a)

    def __str__(self):
        return str(self.id_a)


def solucao_viavel():
    """retorna(viavel: true or false, valor otimo atual)"""
    grupos = dict()
    valor = 0
    global N_PERSONAGENS
    global A_ESCOLHIDOS
    global L_GRUPOS

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


def corte_viabilidade():
    """retorna true or false para fazer o corte de viabilidade"""
    global A_ESCOLHIDOS
    global A_FALTAM
    global L_GRUPOS

    grupos = dict()
    for ator in A_ESCOLHIDOS:
        # conta o numero de grupos que já foi satisfeito
        for grupo_indice in ator.grupos:
            grupos[grupo_indice] = 1

    for ator in A_FALTAM:
        # conta o numero de grupos que já foi satisfeito
        for grupo_indice in ator.grupos:
            grupos[grupo_indice] = 1

    size_e = len(A_ESCOLHIDOS)
    size_f = len(A_FALTAM)

    if (size_e + size_f) < N_PERSONAGENS:
        # se o numero de atores escolhidos+faltantes for menor que o n de personagens total, n é viavel
        return False

    if len(grupos) < L_GRUPOS:
        # se o numero de grupos já escolhidos+faltantes for menor que o n de grupos total, n é viavel
        return False

    return True


def ordena():
    """funcao que devolve uma lista ordenada"""
    global A_FALTAM
    # alterar no futuro para buscar melhorias
    faltam = A_FALTAM.copy()
    return faltam.sort()


def limitante_dada():
    """faz o calculo do valor total com a limitante do professor"""
    global A_ESCOLHIDOS
    global N_PERSONAGENS

    v_total = 0
    for ator in A_ESCOLHIDOS:
        v_total += ator.valor
    menor = ordena()[0]
    v_total += (N_PERSONAGENS - len(A_ESCOLHIDOS)) * menor
    return v_total


def limitante_alunas():
    """faz o calculo do valor total com a limitante feita"""
    global A_ESCOLHIDOS
    global A_FALTAM
    global N_PERSONAGENS
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

    indice = 1
    for i in range(M_ATORES):
        linha = entrada[indice].split(" ")
        ator_v = int(linha[0])
        ator_s = int(linha[1])
        grupos = []
        indice += 1

        for j in range(ator_s):
            grupos.append(int(entrada[indice]))
            indice += 1
        atores.append(Ator(ator_v, grupos, i + 1))


def busca_elenco():
    """backtraing para buscar o elenco"""
    global OPT_VALOR
    global Xopt
    global C_VIABILIDADE
    global C_OTIMALIDADE
    global A_FALTAM
    global A_ESCOLHIDOS
    # verifica se é viavel

    (viavel, nova_solucao_otima) = solucao_viavel()

    # se é viavel, atualiza os valores da solucao
    if viavel:
        if nova_solucao_otima < OPT_VALOR:
            OPT_VALOR = nova_solucao_otima
            print(nova_solucao_otima)
            Xopt = A_ESCOLHIDOS
    # nao tem mais atores para verificar
    if len(A_FALTAM) == 0:
        return

    # verifica se há corte de viabilidade
    if C_VIABILIDADE:
        corte_v = corte_viabilidade()
        if corte_v:
            return
    # verifica se ja corte de otimalidade
    if C_OTIMALIDADE:
        v_atual = OPT_VALOR
        # verifica qual é a funcao limitante
        if LIMITANTE_DADA:
            v_atual = limitante_dada()
        else:
            v_atual = limitante_alunas()

        if v_atual >= OPT_VALOR:
            return
    # ainda falta escolher atores
    ator = A_FALTAM.pop(0)
    # decido não escolher o próximo ator
    busca_elenco()
    # decido escolher o próximo ator
    A_ESCOLHIDOS.append(ator)
    busca_elenco()


def main():
    """inicio com a leitura"""
    global OPT_VALOR
    global LIMITANTE_DADA
    global Xopt
    OPT_VALOR = sys.maxsize

    # se eh a funcao dos alunos, faz uma ordenacao nos valores
    start_time = time.time()
    leitura()

    if not LIMITANTE_DADA:
        atores.sort(key=lambda x: x.valor)

    # backtracking recursivo
    busca_elenco()
    time_end = time.time()

    if len(Xopt) != 0:
        Xopt.sort(key=lambda x: x.id)
        print(" ".join(str(x) for x in Xopt))
        print(OPT_VALOR)
    else:
        print("Inviável")
    print("time: ", str(time_end - start_time), file=sys.stderr)


if __name__ == "__main__":
    for arg in sys.argv:
        if arg == "-a":
            LIMITANTE_DADA = True
        if arg == "-f":
            C_VIABILIDADE = False
        if arg == "-o":
            C_OTIMALIDADE = False
    main()
