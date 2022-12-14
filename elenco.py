#!/usr/bin/python3
import sys
import time


OPT = sys.maxsize
X_OPT = []
ATORES = []
L_GRUPOS = 0
M_ATORES = 0
N_PERSONAGENS = 0
# argumentos da linha de comando
LIMITANTE_DADA = False
C_VIABILIDADE = True
C_OTIMALIDADE = True
NUM_CORTES_OTIMALIDADE = 0
NUM_CORTES_VIABILIDADE = 0
NUM_NOS = 0


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


def main():
    """inicio com a leitura"""

    leitura()
    a_escolhidos = []

    time_start = time.time()

    busca_elenco_bb(a_escolhidos, ATORES)
    time_end = time.time()

    if len(X_OPT) != 0:
        X_OPT.sort(key=lambda x: x.id_a)
        print(" ".join(str(x) for x in X_OPT))
        print(OPT)
    else:
        print("Soluçao inviável")

    print("Número de nós: ", NUM_NOS)
    print("Número de cortes por viabilidade: ", NUM_CORTES_VIABILIDADE)
    print("Número de cortes por otimalidade: ", NUM_CORTES_OTIMALIDADE)
    print("Tempo de execução: ", str(time_end - time_start), file=sys.stderr)


def leitura():
    """Lê todos os dados de entrada"""
    global L_GRUPOS
    global M_ATORES
    global N_PERSONAGENS

    entrada = sys.stdin.readlines()
    # leitura dos valores iniciais
    for i, linha in enumerate(entrada):
        entrada[i] = linha.replace("\n", "")
    linha = entrada[0].split(" ")
    # salva os valores de l m n
    L_GRUPOS = int(linha[0])
    M_ATORES = int(linha[1])
    N_PERSONAGENS = int(linha[2])

    indice = 1

    for i in range(M_ATORES):
        linha = entrada[indice].split(" ")
        # salva os valores de e grupos do ator
        a_valor = int(linha[0])
        a_s = int(linha[1])

        grupos = []
        indice += 1

        for _ in range(a_s):
            # salva os indices dos grupos na qual o ator pertence
            grupos.append(int(entrada[indice]))
            indice += 1

        ATORES.append(Ator(a_valor, grupos, i + 1))


def limitante_dada(a_escolhidos, f_faltam):
    """faz o calculo do valor total com a limitante do professor"""
    total = 0

    for ator in a_escolhidos:
        total += ator.valor

    total += (N_PERSONAGENS - len(a_escolhidos)) * ordena(f_faltam)
    return total


def limitante_aluna(a_escolhidos, f_faltam):
    """faz o calculo do valor total com a limitante feita"""
    size_e = len(a_escolhidos)
    size_f = len(f_faltam)

    total = 0
    for ator in a_escolhidos:
        total += ator.valor

    i = 0
    # ordena os atores pelo menor valor que cobram
    f_faltam.sort(key=lambda x: x.valor)
    # enquanto ainda tem personagens para avaliar o preco
    # e o numero de escolhidos é menor que o total
    # salva os menores valores dos atores
    while size_e < N_PERSONAGENS and i < size_f:
        total += f_faltam[i].valor
        size_e += 1
        i += 1

    return total


def ordena(atores):
    """funcao que devolve 1o valor de uma lista ordenada"""
    if len(atores) == 0:
        return 0
    ator_ordenado = atores.copy()
    ator_ordenado.sort(key=lambda x: x.valor)
    menor_valor = ator_ordenado[0].valor
    return menor_valor


def solucao_viavel(a_escolhidos):
    """retorna(viavel: true or false, valor otimo atual)"""

    # se o numero de atores escolhidos nao é o mesmo que o numero de personagens
    # entao nao é #uma solucao viavel
    if len(a_escolhidos) != N_PERSONAGENS:
        return False

    grupos = dict()
    # salva todos os grupos dos atores já escolhidos
    for ator in a_escolhidos:
        for n_grupo in ator.grupos:
            grupos[n_grupo] = 1

    # se o numero de grupos dos escolhidos nao satisfaz o numero de grupos totais
    if len(grupos) != L_GRUPOS:
        return False

    return True


def calc_valores_otimos(a_escolhidos):
    """faz o calculo dos valores dos atores, caso seja uma solucao viavel"""
    soma_valores = 0

    for ator in a_escolhidos:
        soma_valores += ator.valor
    return soma_valores


def busca_elenco_bb(a_escolhidos, f_faltam):
    """backtraing para buscar o elenco"""
    global OPT
    global X_OPT
    global NUM_CORTES_OTIMALIDADE
    global NUM_CORTES_VIABILIDADE
    global NUM_NOS
    # ATUALIZA O NUMERO DE NÓS
    NUM_NOS += 1

    viavel = solucao_viavel(a_escolhidos)
    if viavel:
        # caso seja viavel, busca o novo conjunto de solucoes otimas
        novo_val = calc_valores_otimos(a_escolhidos)
        if novo_val < OPT:
            OPT = novo_val
            X_OPT = a_escolhidos

    if len(f_faltam) == 0:
        return

    if C_VIABILIDADE:
        NUM_CORTES_VIABILIDADE += 1
        if corte_viabilidade(a_escolhidos, f_faltam):
            return

    if C_OTIMALIDADE:
        NUM_CORTES_OTIMALIDADE += 1
        valor_otimo = OPT
        if LIMITANTE_DADA:
            valor_otimo = limitante_dada(a_escolhidos, f_faltam)
        else:
            valor_otimo = limitante_aluna(a_escolhidos, f_faltam)
        if valor_otimo >= OPT:
            return

    escolhidos = a_escolhidos.copy()
    faltam = f_faltam.copy()
    ator = faltam.pop(0)

    busca_elenco_bb(escolhidos, faltam)

    escolhidos.append(ator)
    busca_elenco_bb(escolhidos, faltam)


def corte_viabilidade(a_escolhidos, f_faltam):
    """retorna true or false para fazer o corte de viabilidade"""
    # faz o corte pois o numero dos atores nao satisfaz o numero de personagens
    if len(f_faltam) + len(a_escolhidos) < N_PERSONAGENS:
        return True

    grupos = dict()
    # busca todos os grupos que já foram preenchidos
    for ator in a_escolhidos:
        for n_grupo in ator.grupos:
            grupos[n_grupo] = 1

    for ator in f_faltam:
        for n_grupo in ator.grupos:
            grupos[n_grupo] = 1

    # se todos os grupos preenchidos nao equivale ao numero de grupos total
    # entao nao é viavel
    if len(grupos) != L_GRUPOS:
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
