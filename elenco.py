#!/usr/bin/python3
import sys
# variavel com o valor solucao otimo
OPT = sys.maxsize 

#conjunto de atores com solucao otima
Xopt = []
atores = []
a_faltam = []
a_escolhidos = []

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

def solucao_viavel(a_escolhidos):
    """retorna(viavel: true or false, valor otimo atual)"""
    grupos = dict()
    valor = 0

    if(len(a_escolhidos)!=n):
        # se n de escolhidos nao satisfaz o numero de personagens necessarios
        return (False, 0)

    for ator in a_escolhidos:
        # soma dos valores de atores já escolhidos
        valor+=ator.valor
        # conta o numero de grupos que já foi satisfeito
        for grupo_indice in ator.grupos:
            grupos[grupo_indice]=1
    
    if(len(grupos)!=l):
        # se o numero total de grupos dos escolhidos nao for o numero total de grupos, nao é viavel
        return (False, 0)

    return (True, valor)
    


def corte_viabilidade(a_escolhidos, a_faltam):
    grupos = dict()
    for ator in a_escolhidos:
        # conta o numero de grupos que já foi satisfeito
        for grupo_indice in ator.grupos:
            grupos[grupo_indice]=1

    for ator in a_faltam:
      # conta o numero de grupos que já foi satisfeito
      for grupo_indice in ator.grupos:
          grupos[grupo_indice]=1

    size_E = len(a_escolhidos)
    size_F = len(a_faltam)

    if((size_E+size_F)<n):
        # se o numero de atores escolhidos+faltantes for menor que o n de personagens total, n é viavel
        return False
        
    if(len(grupos) < l):
        # se o numero de grupos já escolhidos+faltantes for menor que o n de grupos total, n é viavel
        return False

    return True

def min(a_faltam):
    # alterar no futuro para buscar melhorias
    faltam = a_faltam.copy()
    return faltam.sort()



def limitante_dada(a_escolhidos, a_faltam):
    v_total = 0
    for ator in a_escolhidos:
        v_total+=ator.valor
    menor = min(a_faltam)
    v_total+= (n-len(a_escolhidos))*menor[0]
    return v_total


def limitante_alunas(a_escolhidos, a_faltam):
    v_total = 0
    for ator in a_escolhidos:
        v_total+=ator.valor


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
    (viavel, nova_solucao_otima) = solucao_viavel(a_escolhidos)
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
        corte_v= corte_viabilidade(a_escolhidos, a_faltam)
        if corte_v:
            return      
    # verifica se ja corte de otimalidade
    if C_OTIMALIDADE:
        # verifica qual é a funcao limitante
        if LIMITANTE_DADA:
            v_atual = limitante_dada(a_escolhidos, a_faltam)
        else:
            v_atual = limitante_alunas(a_escolhidos, a_faltam)

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




if __name__ == "__main__":
    for arg in sys.argv:
        if arg == "-a":
            LIMITANTE_DADA  = True
        if arg == "-f":
            C_VIABILIDADE = False
        if arg == "-o":
            C_OTIMALIDADE = False
    main()