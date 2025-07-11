import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
from math import sqrt

# Parâmetros iniciais
POPULACAO = 400
INTERACOES = 50
K = 8     # vizinhos no modelo de Watts-Strogatz Moore: 1x1=4 2x2=8 VonNueman: (1x1=8) 2x2=24
P = 0.1   # probabilidade de reconexão

# Estados
ESTADOS = {
    0: "S",  # susceptible
    1: "E",  # contactor
    2: "I",  # disseminator
    3: "R",  # forgetter
    4: "Q",  # quitter
}

class Individuo:
    def __init__(self, id, estado, pos):
        self.id = id
        self.estado = estado
        self.pos = pos  # posição (x, y)

# Inicializa população com apenas A e P
def inicializar_populacao():
    individuos = []
    tamanho = int(np.sqrt(POPULACAO))  # 20x20
    idx = 0
    for i in range(tamanho):
        for j in range(tamanho):
            estado = 2 if random.random() < 0.05 else 0  # 5% 
            ind = Individuo(idx, estado, (i, j))
            individuos.append(ind)
            idx += 1
    return individuos

# Criação da rede de pequeno mundo
def criar_rede():
    return nx.watts_strogatz_graph(POPULACAO, K, P)

# Simulação principal
def simular():
    rede = criar_rede()
    populacao = inicializar_populacao()
    
    for t in range(INTERACOES):
        print(f"--- Interação {t+1} ---")
        
# Execução
simular()
