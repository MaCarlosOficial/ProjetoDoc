# Esse repositório tem por objetivo armazenar as anotações, informações e códigos sobre as simulações referente ao estudo sobre a distribuição do conhecimento em organizações (KCO).

Todos os artigos utilizados como base de conhecimento e referência, também estão disponíveis no repositório.
O artigo principal utilizado como referência foi o **"Modelling and simulating knowledge diffusion in knowledge collaboration organisations using improved cellular automata"** de Su Jiafu, Zhang Xuefeng, Yang Jiaquan & Qian Xiaoduo.

# 1- Projeto: Implementação do artigo principal na sua forma original
## Introdução

O primeiro projeto (Artigo_KCO.ipynb) é uma implementação em Python Notebook, do modelo de autômatos celulares (AC) descrito no artigo principal.
O objetivo do código é replicar as simulações realizadas pelos autores para estudar como a difusão de conhecimento em Organizações de Colaboraçõo de Conhecimento (KCOs) é influenciada por fatores como a distribuição inicial de conhecimento, a acessibilidade entre indivíduos, a mobilidade e as taxas de desistência.
A simulação modela cada indivíduo da organizaçõo como uma "célula" em um grid 2D, cujo estado de conhecimento evolui ao longo do tempo com base em regras de transições locais, refletindo as interações com seus vizinhos.

## Estrutura do Código
Utilizou-se o paradigma de liguagem estruturado/funcional, que tem como objetivo solucionar problemas a partir da quebra de problemas em problemas menores, denominados sub-rotinas ou subprogramas.
O código está estruturado em uma série de funções que, juntas, constroem e executam o modelo de simulação que representa o problema de pesquisa.
As principais funções do código são:
1.  **Configuração Inicial:** Funções que criam o ambiente da simulação.
2.  **Mecanismos do Modelo:** Funções que implementam as regras e a dinâmica do autômato celular.
3.  **Execução e Análise:** Funções que rodam a simulação e geram os resultados visuais.

## Descrição Detalhada das Funções
A seguir, cada função principal do código é explicada em detalhes.
---
### `def set_up_configuration(normalize=(0,1), distribution_type='random')`

* **Propósito:** Esta função inicializa o ambiente da simulação. Ela cria o grid celular, define a população de 400 indivíduos e atribui a cada um deles seus atributos iniciais, como status de conhecimento e caracterósticas individuais.
* **Relação com o Artigo:**
    * **Espaço Celular (L):** Implementa o grid 2D de 20x20, conforme descrito na Seção 4.1, representando a KCO com 400 indivíduos.
    * **Estado Inicial:** Define o estado inicial da população, com 5% de Disseminadores (I, status 2) e 95% de Suscetóveis (S, status 0), conforme a Seção 4.1.
    * **Padrões de distribuição:** Implementa os três padrões de distribuição inicial para os disseminadores "Distribuição Grid.png" (Figura 3 do artigo): `monopolistic`, `small-group` e `random`.
    * **Heterogeneidade Individual:** Atribui a cada indivíduo capacidades de aprendizado (`learningCapability`) e transferência (`transferCapability`) a partir de uma distribuição Normal, e taxas de esquecimento (`forgettingRate`) e desistência (`quittingRate`) a partir de uma distribuição Uniforme, refletindo a heterogeneidade descrita na Seção 3.3.5.
* **Parâmetros:**
    * `normalize`: Uma tupla que define o intervalo para a geração das taxas de desistência e esquecimento.
    * `distribution_type`: Uma string (`'random'`, `'monopolistic'`, `'small-group'`) que define como os disseminadores iniciais são posicionados no grid.
* **Retorno:** Um DataFrame do `pandas` contendo a população inicial, onde cada linha representa um indivíduo com seus respectivos atributos.

---
### `def mobility(df, MD=20, IM=20, press=False)`

* **Propósito:** Simula o movimento dos indivíduos dentro do grid, permitindo que eles troquem de posição e, consequentemente, de vizinhança.
* **Relação com o Artigo:**
    * **Mobilidade Individual:** Implementa diretamente o mecanismo de "caminhada aleatéria" (random walk CA) descrito na Seção 3.3.6.
    * **Parâmetros MD e IM:** Utiliza os Parâmetros `MD` (Maximum Distance of Movement) e `IM` (Proportion of Mobile Individuals) para controlar a dinâmica do movimento, conforme especificado pelos autores. A simulação utiliza uma fronteira toroidal (`% rows`, `% cols`) para garantir que os movimentos que ultrapassam as bordas do grid reapareçam do lado oposto.
* **Parâmetros:**
    * `df`: O DataFrame da população atual.
    * `MD`: A distância máxima que um indivíduo pode se mover.
    * `IM`: A porcentagem da população que se moverá em cada ciclo.
* **Retorno:** Um novo DataFrame com os atributos dos indivíduos trocados, simulando o efeito da mobilidade.

---
### `def neighborsF(df, point, radius=1, neighbors='Moore')`

* **Propósito:** Identifica as células vizinhas de um determinado indivíduo no grid e calcula a distância euclidiana até elas.
* **Relação com o Artigo:**
    * **vizinhança (V):** Implementa os tipos de vizinhança mencionados na Seção 3.3.3 e ilustrados na Figura 2. A função pode calcular vizinhanças de `Moore` e `Von Neumann` com raios de 1 ou 2.
    * **distância Celular:** O cálculo da distância euclidiana corresponde á fórmula da "distância celular" (Equação 3) usada para ponderar a força da relação de troca de conhecimento.
* **Parâmetros:**
    * `df`: O DataFrame da população.
    * `point`: Uma tupla `(row, col)` com as coordenadas da célula central.
    * `radius`: O raio da vizinhança (1 ou 2).
    * `neighbors`: O tipo de vizinhança (`'Moore'` ou `'VonNeumann'`).
* **Retorno:** Uma lista contendo os índices dos vizinhos no DataFrame e a distância euclidiana até cada um deles.

---
### `def acquisition_rate(df, idx_current, radius, neighbors)`

* **Propósito:** Calcula a taxa máxima de aquisição de conhecimento para um indivíduo Suscetível (S) ou Esquecedor (R).
* **Relação com o Artigo:**
    * **Taxa de aquisição de Conhecimento:** Implementa a fórmula da taxa de aquisição de conhecimento (Equação 4, Seção 3.3.4). O cálculo considera a `learningCapability` do indivíduo atual, a `transferCapability` de seus vizinhos Disseminadores (status 2) e a `distância celular` entre eles.
    * **Estratégia de Troca:** A função busca a taxa *máxima* entre todos os vizinhos disseminadores, conforme especificado pela função `max` na Equação 4, refletindo uma estratégia racional de aprendizado.
* **Parâmetros:**
    * `df`: O DataFrame da população.
    * `idx_current`: O índice do indivíduo cuja taxa está sendo calculada.
    * `radius`, `neighbors`: Parâmetros para definir a vizinhança.
* **Retorno:** Um valor `float` que representa a máxima probabilidade de aquisição de conhecimento para o indivíduo.

---
### `def transition_F(df, radius, neighbors)`

* **Propósito:** Esta é a função central do autômato celular, que aplica as regras de transição para atualizar o estado de cada indivíduo a cada ciclo de tempo.
* **Relação com o Artigo:**
    * **Função de Transição (F):** Representa a implementaçõo completa das regras de transição de estado descritas na Seção 3.3.4 e 3.3.5, e visualizadas na Figura 1.
    * **Transições de Estado:**
        1.  **S é E** e **R é E:** Utiliza a `acquisition_rate()` e um sorteio aleatório para determinar se um Suscetível ou Esquecedor se torna um Contatante.
        2.  **E é {I, R, Q}:** Para um Contatante, calcula as taxas de absorção (`Il`), esquecimento (`Rl`) e desistência (`Ql`) ajustadas pelo número de vezes que o indivíduo já foi contatante (`D`), conforme as fórmulas $R'_L = R_L^{(D+1)}$ e $Q'_L = Q_L^{(D+1)}$ (Seção 3.3.5). Um sorteio aleatório decide o próximo estado.
* **Parâmetros:**
    * `df`: O DataFrame da população no estado atual.
    * `radius`, `neighbors`: Parâmetros da vizinhança.
* **Retorno:** Um novo DataFrame com os status dos indivíduos atualizados para o próximo ciclo de tempo.

---
### `def simular_difusao(df, MD=20, IM=50, radius=1, neighbors='Moore', press=False)`

* **Propósito:** Orquestra a simulação completa, executando o loop principal por um número definido de ciclos (iterações).
* **Relação com o Artigo:**
    * **Processo de simulação:** Executa a simulação por 50 "semanas" (ciclos), conforme mencionado na Seção 4.1. Em cada ciclo, aplica primeiro a função de transição (`transition_F`) e depois a função de mobilidade (`mobility`), seguindo a lógica do modelo de AC aprimorado.
* **Parâmetros:**
    * `df`: O DataFrame da configuraçõo inicial.
    * Todos os outros Parâmetros (`MD`, `IM`, `radius`, etc.) são passados para as funções internas.
* **Retorno:** Um DataFrame contendo o histórico das estatísticas (contagem de indivíduos em cada estado) para cada ciclo da simulação.

---
### `def plot_results(...)` e `run_experiment_figure_X(...)`

* **Propósito:**
    * `plot_results`: Uma função genérica para visualizar os resultados das simulações, criando gráficos que replicam o estilo dos apresentados no artigo.
    * `run_experiment_figure_X`: Funções específicas (`run_experiment_figure_4`, `run_experiment_figure_6`, etc.) que configuram e executam as simulações para replicar cada um dos experimentos e figuras do artigo.
* **Relação com o Artigo:**
    * **Métricas de Desempenho:** A função `plot_results` calcula e plota as duas métricas de avaliação definidas na Seção 4.1: a proporção de disseminadores ($r_t$, Equação 5) e a velocidade de difusão ($v_t$, Equação 6).
    * **Replicaçõo dos Experimentos:** As funções `run_experiment_...` automatizam a execuçõo de múltiplas rodadas para cada cenário experimental (50 vezes, conforme Seção 4.1), calculando a média dos resultados para garantir robustez estatística, uma prática padrão em estudos de simulação.
* **Parâmetros:** Variam de acordo com o experimento, ajustando `distribution_type`, `radius`, `neighbors`, `MD`, `IM` e o intervalo das taxas de desistência para corresponder ás condições de cada figura do artigo.
* **Retorno:** Nenhuma. As funções salvam os gráficos gerados em arquivos de imagem com os nomes: figura_4_simulacao.png, figura_5_simulacao.png, figura_6_simulacao.png, figura_7_simulacao.png e figura_8_simulacao.png, conforme figuras apresentadas no artigo.

# 2- Projeto: Implementação da simulação usando Redes de Pequeno Mundo (Small Wold Networks-SWN)
## Introdução

Este projeto (SWN_KCO.ipynb) é uma implementação em Python Notebook, do modelo descrito no artigo principal, utilizando Redes de Pequeno Mundo (SWN) para simulação dos objetivos do artigo original, com o objetivo de estudar o comportamento utilizando outros modelos de distribição.
A simulação modela cada indivíduo da organizaçõo como uma "nó" em um grafo, cujo estado de conhecimento evolui ao longo do tempo com base em regras de transições locais e globais, refletindo as interações com seus nós vizinhos.

## Estrutura do Código
Segue os mesmos paradigmas do primeiro projeto:
1.  **Configuração Inicial:** Funções que criam o ambiente da simulação.
2.  **Mecanismos do Modelo:** Funções que implementam as regras e a dinâmica do autômato celular.
3.  **Execução e Análise:** Funções que rodam a simulação e geram os resultados visuais.

## Descrição Detalhada das Funções
A seguir, cada função principal do código é explicada em detalhes.
---
### `def set_up_configuration(normalize=(0,1), distribution_type='random')`

* **Propósito:** Esta função inicializa o ambiente da simulação. Ela cria o grid celular, define a população de 400 indivíduos e atribui a cada um deles seus atributos iniciais, como status de conhecimento e caracterósticas individuais.
* **Relação com o Artigo:**
    * **Espaço Celular (L):** Implementa o grid 2D de 20x20, conforme descrito na Seção 4.1, representando a KCO com 400 indivíduos.
    * **Estado Inicial:** Define o estado inicial da população, com 5% de Disseminadores (I, status 2) e 95% de Suscetóveis (S, status 0), conforme a Seção 4.1.
    * **Padrões de distribuição:** Implementa os três padrões de distribuição inicial para os disseminadores "Distribuição Grid.png" (Figura 3 do artigo): `monopolistic`, `small-group` e `random`.
    * **Heterogeneidade Individual:** Atribui a cada indivíduo capacidades de aprendizado (`learningCapability`) e transferência (`transferCapability`) a partir de uma distribuição Normal, e taxas de esquecimento (`forgettingRate`) e desistência (`quittingRate`) a partir de uma distribuição Uniforme, refletindo a heterogeneidade descrita na Seção 3.3.5.
* **Parâmetros:**
    * `normalize`: Uma tupla que define o intervalo para a geração das taxas de desistência e esquecimento.
    * `distribution_type`: Uma string (`'random'`, `'monopolistic'`, `'small-group'`) que define como os disseminadores iniciais são posicionados no grid.
* **Retorno:** Um DataFrame do `pandas` contendo a população inicial, onde cada linha representa um indivíduo com seus respectivos atributos.

---
### `def mobility(df, MD=20, IM=20, press=False)`

* **Propósito:** Simula o movimento dos indivíduos dentro do grid, permitindo que eles troquem de posição e, consequentemente, de vizinhança.
* **Relação com o Artigo:**
    * **Mobilidade Individual:** Implementa diretamente o mecanismo de "caminhada aleatéria" (random walk CA) descrito na Seção 3.3.6.
    * **Parâmetros MD e IM:** Utiliza os Parâmetros `MD` (Maximum Distance of Movement) e `IM` (Proportion of Mobile Individuals) para controlar a dinâmica do movimento, conforme especificado pelos autores. A simulação utiliza uma fronteira toroidal (`% rows`, `% cols`) para garantir que os movimentos que ultrapassam as bordas do grid reapareçam do lado oposto.
* **Parâmetros:**
    * `df`: O DataFrame da população atual.
    * `MD`: A distância máxima que um indivíduo pode se mover.
    * `IM`: A porcentagem da população que se moverá em cada ciclo.
* **Retorno:** Um novo DataFrame com os atributos dos indivíduos trocados, simulando o efeito da mobilidade.

---
### `def neighborsF(df, point, radius=1, neighbors='Moore')`

* **Propósito:** Identifica as células vizinhas de um determinado indivíduo no grid e calcula a distância euclidiana até elas.
* **Relação com o Artigo:**
    * **vizinhança (V):** Implementa os tipos de vizinhança mencionados na Seção 3.3.3 e ilustrados na Figura 2. A função pode calcular vizinhanças de `Moore` e `Von Neumann` com raios de 1 ou 2.
    * **distância Celular:** O cálculo da distância euclidiana corresponde á fórmula da "distância celular" (Equação 3) usada para ponderar a força da relação de troca de conhecimento.
* **Parâmetros:**
    * `df`: O DataFrame da população.
    * `point`: Uma tupla `(row, col)` com as coordenadas da célula central.
    * `radius`: O raio da vizinhança (1 ou 2).
    * `neighbors`: O tipo de vizinhança (`'Moore'` ou `'VonNeumann'`).
* **Retorno:** Uma lista contendo os índices dos vizinhos no DataFrame e a distância euclidiana até cada um deles.

---
### `def acquisition_rate(df, idx_current, radius, neighbors)`

* **Propósito:** Calcula a taxa máxima de aquisição de conhecimento para um indivíduo Suscetível (S) ou Esquecedor (R).
* **Relação com o Artigo:**
    * **Taxa de aquisição de Conhecimento:** Implementa a fórmula da taxa de aquisição de conhecimento (Equação 4, Seção 3.3.4). O cálculo considera a `learningCapability` do indivíduo atual, a `transferCapability` de seus vizinhos Disseminadores (status 2) e a `distância celular` entre eles.
    * **Estratégia de Troca:** A função busca a taxa *máxima* entre todos os vizinhos disseminadores, conforme especificado pela função `max` na Equação 4, refletindo uma estratégia racional de aprendizado.
* **Parâmetros:**
    * `df`: O DataFrame da população.
    * `idx_current`: O índice do indivíduo cuja taxa está sendo calculada.
    * `radius`, `neighbors`: Parâmetros para definir a vizinhança.
* **Retorno:** Um valor `float` que representa a máxima probabilidade de aquisição de conhecimento para o indivíduo.

---
### `def transition_F(df, radius, neighbors)`

* **Propósito:** Esta é a função central do autômato celular, que aplica as regras de transição para atualizar o estado de cada indivíduo a cada ciclo de tempo.
* **Relação com o Artigo:**
    * **Função de Transição (F):** Representa a implementaçõo completa das regras de transição de estado descritas na Seção 3.3.4 e 3.3.5, e visualizadas na Figura 1.
    * **Transições de Estado:**
        1.  **S é E** e **R é E:** Utiliza a `acquisition_rate()` e um sorteio aleatório para determinar se um Suscetível ou Esquecedor se torna um Contatante.
        2.  **E é {I, R, Q}:** Para um Contatante, calcula as taxas de absorção (`Il`), esquecimento (`Rl`) e desistência (`Ql`) ajustadas pelo número de vezes que o indivíduo já foi contatante (`D`), conforme as fórmulas $R'_L = R_L^{(D+1)}$ e $Q'_L = Q_L^{(D+1)}$ (Seção 3.3.5). Um sorteio aleatório decide o próximo estado.
* **Parâmetros:**
    * `df`: O DataFrame da população no estado atual.
    * `radius`, `neighbors`: Parâmetros da vizinhança.
* **Retorno:** Um novo DataFrame com os status dos indivíduos atualizados para o próximo ciclo de tempo.

---
### `def simular_difusao(df, MD=20, IM=50, radius=1, neighbors='Moore', press=False)`

* **Propósito:** Orquestra a simulação completa, executando o loop principal por um número definido de ciclos (iterações).
* **Relação com o Artigo:**
    * **Processo de simulação:** Executa a simulação por 50 "semanas" (ciclos), conforme mencionado na Seção 4.1. Em cada ciclo, aplica primeiro a função de transição (`transition_F`) e depois a função de mobilidade (`mobility`), seguindo a lógica do modelo de AC aprimorado.
* **Parâmetros:**
    * `df`: O DataFrame da configuraçõo inicial.
    * Todos os outros Parâmetros (`MD`, `IM`, `radius`, etc.) são passados para as funções internas.
* **Retorno:** Um DataFrame contendo o histórico das estatísticas (contagem de indivíduos em cada estado) para cada ciclo da simulação.

---
### `def plot_results(...)` e `run_experiment_figure_X(...)`

* **Propósito:**
    * `plot_results`: Uma função genérica para visualizar os resultados das simulações, criando gráficos que replicam o estilo dos apresentados no artigo.
    * `run_experiment_figure_X`: Funções específicas (`run_experiment_figure_4`, `run_experiment_figure_6`, etc.) que configuram e executam as simulações para replicar cada um dos experimentos e figuras do artigo.
* **Relação com o Artigo:**
    * **Métricas de Desempenho:** A função `plot_results` calcula e plota as duas métricas de avaliação definidas na Seção 4.1: a proporção de disseminadores ($r_t$, Equação 5) e a velocidade de difusão ($v_t$, Equação 6).
    * **Replicaçõo dos Experimentos:** As funções `run_experiment_...` automatizam a execuçõo de múltiplas rodadas para cada cenário experimental (50 vezes, conforme Seção 4.1), calculando a média dos resultados para garantir robustez estatística, uma prática padrão em estudos de simulação.
* **Parâmetros:** Variam de acordo com o experimento, ajustando `distribution_type`, `radius`, `neighbors`, `MD`, `IM` e o intervalo das taxas de desistência para corresponder ás condições de cada figura do artigo.
* **Retorno:** Nenhuma. As funções salvam os gráficos gerados em arquivos de imagem com os nomes: figura_4_simulacao_swn.png, figura_5_simulacao_swn.png, figura_6_simulacao_swn.png, figura_7_simulacao_swn.png e figura_8_simulacao_swn.png.
