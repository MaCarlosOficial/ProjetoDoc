# Esse repositório tem por objetivo armazenar anotações, informações e códigos sobre o estudo da difusão de conhecimento em Organizações de Colaboraçõo de Conhecimento (KCOs) e com ela é influenciada por fatores como a distribuição inicial de conhecimento, a acessibilidade entre indivíduos, a mobilidade e as taxas de desistência. 

Todos os artigos utilizados como base de conhecimento e referência, também estão disponíveis no repositório.
O artigo principal utilizado como referência foi o *"Modelling and simulating knowledge diffusion in knowledge collaboration organisations using improved cellular automata"* de Su Jiafu, Zhang Xuefeng, Yang Jiaquan & Qian Xiaoduo.

# 1- Projeto: Implementação do artigo principal na sua forma original 
## Introdução

Pasta: replica_experimento

O primeiro projeto é uma implementação em Python Notebook, do modelo de autômatos celulares (AC) descrito no artigo principal.
O objetivo do código é replicar as simulações realizadas pelos autores para estudar como a difusão de conhecimento em Organizações de Colaboração de Conhecimento (KCOs) é influenciada por fatores como a distribuição inicial de conhecimento, a acessibilidade entre indivíduos, a mobilidade e as taxas de desistência.
A simulação modela cada indivíduo da organizaçõo como uma "célula" em um grid 2D, cujo estado de conhecimento evolui ao longo do tempo com base em regras de transições locais, refletindo as interações com seus vizinhos.

# 2- Projeto: Implementação da simulação usando Redes de Pequeno Mundo (Small Wold Networks-SWN)
## Introdução

Pasta: SWN

Este projeto é uma implementação em Python Notebook, do modelo descrito no artigo principal, utilizando Redes de Pequeno Mundo (SWN) para simulação dos objetivos do artigo original, com o objetivo de estudar o comportamento utilizando outros modelos de distribição.
A simulação modela cada indivíduo da organização como um "nó" em um grafo, cujo estado de conhecimento evolui ao longo do tempo com base em regras de transições locais e globais, refletindo as interações com seus nós vizinhos.
