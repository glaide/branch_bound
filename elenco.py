from re import L
import sys

OPT = sys.maxsize
Xopt = []
atores = []
CONTADOR = 0
l = 0      # num de grupos
m = 0        # num de atores
n = 0        # num de personagens
# argumentos:
LIMITANTE_DADA    = False # usar função limitante dos profs.
C_VIABILIDADE   = True  # cortes de viabilidade
C_OTIMALIDADE   = True  # cortes de otimalidade

class Ator:
    """atributos: valor, grupos na qual pertence e indice dos mesmos"""
    def __init__(self, valor,indice, grupos):
        self.valor = valor
        self.g_indice = indice
        self.grupos = grupos

    def __repr__(self):
        return str(self.g_indice)

    def __str__(self):
        return str(self.g_indice)

def main():
    """inicio com a leitura"""
    leitura()



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
        atores.append(Ator(ator_v, ator_s, grupos))   

if __name__ == "__main__":
    for arg in sys.argv:
        if arg == "-a":
            LIMITANTE_DADA  = True
        if arg == "-f":
            C_VIABILIDADE = False
        if arg == "-o":
            C_OTIMALIDADE = False

    main()