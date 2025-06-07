import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
from math import sqrt

# Parâmetros iniciais
POPULACAO = 400
K = 6                 # vizinhos no modelo de Watts-Strogatz
P = 0.1               # probabilidade de reconexão
INTERACOES = 50
DMM = 2               # distância máxima de mobilidade
PIM = 0.1             # proporção de indivíduos móveis

# Estados
ESTADOS = {
    0: "A",  # Aluno
    1: "E",  # Aluno de DP
    2: "P",  # Professor
    3: "R",  # Aluno Reprovado
    4: "Q",  # Aluno Desistente
}

class Individuo:
    def __init__(self, id, estado, pos):
        self.id = id
        self.estado = estado
        self.pos = pos  # posição (x, y)
        self.TxA = np.random.rand()
        self.TxT = np.random.rand() if estado == 2 else 0
        self.TxE = 0
        self.TxD = 0
        self.D = 0  # número de vezes que foi reprovado

    def calcula_txE_txD(self):
        if self.estado in [0, 1]:
            self.TxE = 1 - self.TxA
            self.TxD = 1 - self.TxE - self.TxA

# Inicializa população com apenas A e P
def inicializar_populacao():
    individuos = []
    tamanho = int(np.sqrt(POPULACAO))  # 20x20
    idx = 0
    for i in range(tamanho):
        for j in range(tamanho):
            estado = 2 if random.random() < 0.1 else 0  # 10% professores
            ind = Individuo(idx, estado, (i, j))
            ind.calcula_txE_txD()
            individuos.append(ind)
            idx += 1
    return individuos

def distancia(ind1, ind2):
    x1, y1 = ind1.pos
    x2, y2 = ind2.pos
    return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)

# Criação da rede de pequeno mundo
def criar_rede():
    return nx.watts_strogatz_graph(POPULACAO, K, P)

# Simulação principal
def simular():
    rede = criar_rede()
    populacao = inicializar_populacao()
    
    for t in range(INTERACOES):
        print(f"--- Interação {t+1} ---")
        
        # Mobilidade
        movimentar_individuos(populacao, DMM, PIM)

        # Interação e Transição de Conhecimento
        atualizar_estados(rede, populacao)

        # Visualização 
        # visualizar_estado(rede, populacao)

# Mobilidade baseada em DMM e PIM
def movimentar_individuos(populacao, DMM, PIM):
    qtd_moveis = int(POPULACAO * PIM)
    tamanho = int(np.sqrt(POPULACAO))
    for _ in range(qtd_moveis):
        ind = random.choice(populacao)
        x, y = ind.pos
        dx = random.randint(-DMM, DMM)
        dy = random.randint(-DMM, DMM)
        nx, ny = max(0, min(x + dx, tamanho - 1)), max(0, min(y + dy, tamanho - 1))
        
        # encontra quem está na posição (nx, ny)
        alvo = next((a for a in populacao if a.pos == (nx, ny)), None)
        if alvo:
            ind.pos, alvo.pos = alvo.pos, ind.pos  # troca posições

# Atualização dos estados com base nas regras
def atualizar_estados(populacao, raio_vizinhanca=2.0):
    for ind in populacao:
        if ind.estado == 0:  # Aluno suscetível
            for viz in populacao:
                if viz.estado == 2:  # Professor
                    dist = distancia(ind, viz)
                    if dist <= raio_vizinhanca:
                        tac = (1 / dist) * sqrt(viz.TxT * ind.TxA)
                        if random.random() < tac:
                            ind.estado = 1  # vira Aluno de DP
                            break

# Execução
simular()
