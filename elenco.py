#!/usr/bin/python3
import sys
# variavel com o valor solucao otimo
OPT = sys.maxsize 

#conjunto de atores com solucao otima
Xopt = []
atores = []

l = 0       # num de grupos
m = 0       # num de atores
n = 0       # num de personagens
count = 0
# argumentos:
LIMITANTE_DADA    = False # usar função limitante dos profs.
C_VIABILIDADE   = True  # cortes de viabilidade
C_OTIMALIDADE   = True  # cortes de otimalidade
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
    """inicio com a leitura"""

    leitura()
    a_escolhidos = []
    # se eh a funcao dos alunos, faz uma ordenacao nos valores
    if not LIMITANTE_DADA:
      atores.sort(key=lambda x: x.valor)
    busca_elenco(a_escolhidos, atores)

def busca_elenco(a_escolhidos, a_faltam):
    # verifica se é viavel
    (viavel, nova_solucao_otima) = viabilidade()
    # se é viavel, atualiza os valores da solucao
    if viavel:
        if nova_solucao_otima < OPT:
            OPT = nova_solucao_otima
            Xopt = a_escolhidos
    # nao tem mais atores para verificar
    if not len(atores):
      return
    
    # verifica se há corte de viabilidade
    if C_VIABILIDADE:
        # chama funcao de corte_viabilidade
      
    # verifica se ja corte de otimalidade
    if C_OTIMALIDADE:
        # verifica qual é a funcao limitante
        if LIMITANTE_DADA:
            # chama funcao do professor
        else:
            # faz com funcao dos alunos
        if (v_atual >= OPT):
           return
    # ainda falta escolher atores        
    e = a_escolhidos.copy()
    f = a_faltam.copy()
    ator = f.pop(0)
    # decido não escolher o próximo ator
    busca_elenco(e,f)
    # decido escolher o próximo ator
    e.append(ator)
    busca_elenco(e,f)


# def viabilidade():

def leitura():
    """"Lê todos os dados de entrada"""

    # leitura dos valores iniciais
    entrada = sys.stdin.readlines()
    for i, linha in enumerate(entrada):
       entrada[i] = linha.replace("\n", "")
    linha = entrada[0].split(" ")
    l = int(linha[0]) # num de grupos
    m = int(linha[1]) # num de atores
    n = int(linha[2]) # num de personagens
    for i in range(m):
        linha = entrada[i+1].split(" ")
        ator_v = int(linha[0])
        ator_s = int(linha[1])
        grupos = []
        for j in range(ator_s):
            grupos.append(j+1)
        atores.append(Ator(ator_v,  grupos, i+1))  


if __name__ == "__main__":
    for arg in sys.argv:
        if arg == "-a":
            LIMITANTE_DADA  = True
        if arg == "-f":
            C_VIABILIDADE = False
        if arg == "-o":
            C_OTIMALIDADE = False
    main()