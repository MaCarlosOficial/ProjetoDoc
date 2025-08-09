# Esse reposit�rio tem por objetivo armazenar as anota��es, informa��es e c�digos sobre as simula��es referente a distribui��o do conhecimento em organiza��es (KCO).

Todos os artigos utilizados como base de conhecimento e refer�ncia, tamb�m est�o dispon�veis no reposit�rio.
Artigo principal de refer�ncia: Modelling and simulating knowledge diffusion in knowledge collaboration organisations using improved cellular automata.


1 - Replicar simula��o do artigo principal.
    Para replicar o experimento realizado pelo artigo, foi implementado um
    Cada parte do problema foi desmembrado em fun��es para melhorar a interpretado do conhecimento do problema de pesquisa, como um todo.
    - Fun��o set_up_configuration.
      Esta fun��o � respons�vel por criar a configura��o inicial do GRID. Essa fun��o ser� respons�vel pela inicializa��o de cada par�metro com base no par�metros de entrada fornecidos, al�m da cria��o dos 3 tipos de distribui��o da popula��o relatada no artigo (Randomica, Pequenos grupos e monopolistica).
    - Fun��o


## Introdu��o

[cite_start]Este projeto � uma implementa��o em Python Notebook, do modelo de aut�matos celulares (AC) descrito no artigo **"Modelling and simulating knowledge diffusion in knowledge collaboration organisations using improved cellular automata"** de Su Jiafu, Zhang Xuefeng, Yang Jiaquan & Qian Xiaoduo.
[cite_start]O objetivo do c�digo � replicar as simula��es realizadas pelos autores para estudar como a difus�o de conhecimento em Organiza��es de Colabora��o de Conhecimento (KCOs) � influenciada por fatores como a distribui��o inicial de conhecimento, a acessibilidade entre indiv�duos, a mobilidade e as taxas de desist�ncia.
[cite_start]A simula��o modela cada indiv�duo da organiza��o como uma "c�lula" em um grid 2D, cujo estado de conhecimento evolui ao longo do tempo com base em regras de transi��o locais, refletindo as intera��es com seus vizinhos.

## Estrutura do C�digo
Utilizou-se o paradigma de liguagem estruturado/funcional, que tem como objetivo solucionar problemas a partir da quebra de problemas em problemas menores, denominados sub-rotinas ou subprogramas.
O c�digo est� estruturado em uma s�rie de fun��es que, juntas, constroem e executam o modelo de simula��o que representa o problema de pesquisa.
1.  **Configura��o Inicial:** Fun��es que criam o ambiente da simula��o.
2.  **Mecanismos do Modelo:** Fun��es que implementam as regras e a din�mica do aut�mato celular.
3.  **Execu��o e An�lise:** Fun��es que rodam a simula��o e geram os resultados visuais.

## Descri��o Detalhada das Fun��es
A seguir, cada fun��o principal do c�digo � explicada em detalhes.
---
### `def set_up_configuration(normalize=(0,1), distribution_type='random')`

* **Prop�sito:** Esta fun��o inicializa o ambiente da simula��o. [cite_start]Ela cria o grid celular, define a popula��o de 400 indiv�duos e atribui a cada um deles seus atributos iniciais, como status de conhecimento e caracter�sticas individuais[cite: 2731].
* **Rela��o com o Artigo:**
    * [cite_start]**Espa�o Celular (L):** Implementa o grid 2D de 20x20, conforme descrito na Se��o 4.1, representando a KCO com 400 indiv�duos[cite: 2652, 2731].
    * [cite_start]**Estado Inicial:** Define o estado inicial da popula��o, com 5% de Disseminadores (I, status 2) e 95% de Suscet�veis (S, status 0), conforme a Se��o 4.1[cite: 2751, 3079].
    * [cite_start]**Padr�es de Distribui��o:** Implementa os tr�s padr�es de distribui��o inicial para os disseminadores (Figura 3 do artigo): `monopolistic`, `small-group` e `random`[cite: 2733].
    * [cite_start]**Heterogeneidade Individual:** Atribui a cada indiv�duo capacidades de aprendizado (`learningCapability`) e transfer�ncia (`transferCapability`) a partir de uma distribui��o Normal, e taxas de esquecimento (`forgettingRate`) e desist�ncia (`quittingRate`) a partir de uma distribui��o Uniforme, refletindo a heterogeneidade descrita na Se��o 3.3.5[cite: 2696, 2708, 2694, 3088].
* **Par�metros:**
    * `normalize`: Uma tupla que define o intervalo para a gera��o das taxas de desist�ncia e esquecimento.
    * `distribution_type`: Uma string (`'random'`, `'monopolistic'`, `'small-group'`) que define como os disseminadores iniciais s�o posicionados no grid.
* **Retorno:** Um DataFrame do `pandas` contendo a popula��o inicial, onde cada linha representa um indiv�duo com seus respectivos atributos.

---

### `def mobility(df, MD=20, IM=20, press=False)`

* **Prop�sito:** Simula o movimento dos indiv�duos dentro do grid, permitindo que eles troquem de posi��o e, consequentemente, de vizinhan�a.
* **Rela��o com o Artigo:**
    * [cite_start]**Mobilidade Individual:** Implementa diretamente o mecanismo de "caminhada aleat�ria" (random walk CA) descrito na Se��o 3.3.6[cite: 2714].
    * [cite_start]**Par�metros MD e IM:** Utiliza os par�metros `MD` (Maximum Distance of Movement) e `IM` (Proportion of Mobile Individuals) para controlar a din�mica do movimento, conforme especificado pelos autores[cite: 2718]. A simula��o utiliza uma fronteira toroidal (`% rows`, `% cols`) para garantir que os movimentos que ultrapassam as bordas do grid reapare�am do lado oposto.
* **Par�metros:**
    * `df`: O DataFrame da popula��o atual.
    * [cite_start]`MD`: A dist�ncia m�xima que um indiv�duo pode se mover[cite: 2718].
    * [cite_start]`IM`: A porcentagem da popula��o que se mover� em cada ciclo[cite: 2718].
* **Retorno:** Um novo DataFrame com os atributos dos indiv�duos trocados, simulando o efeito da mobilidade.

---

### `def neighborsF(df, point, radius=1, neighbors='Moore')`

* **Prop�sito:** Identifica as c�lulas vizinhas de um determinado indiv�duo no grid e calcula a dist�ncia euclidiana at� elas.
* **Rela��o com o Artigo:**
    * [cite_start]**Vizinhan�a (V):** Implementa os tipos de vizinhan�a estendidos mencionados na Se��o 3.3.3 e ilustrados na Figura 2[cite: 2667, 2669]. [cite_start]A fun��o pode calcular vizinhan�as de `Moore` e `Von Neumann` com raios de 1 ou 2[cite: 2668, 2801].
    * [cite_start]**Dist�ncia Celular:** O c�lculo da dist�ncia euclidiana corresponde � f�rmula da "dist�ncia celular" (Equa��o 3) usada para ponderar a for�a da rela��o de troca de conhecimento[cite: 2660].
* **Par�metros:**
    * `df`: O DataFrame da popula��o.
    * `point`: Uma tupla `(row, col)` com as coordenadas da c�lula central.
    * `radius`: O raio da vizinhan�a (1 ou 2).
    * `neighbors`: O tipo de vizinhan�a (`'Moore'` ou `'VonNeumann'`).
* **Retorno:** Uma lista contendo os �ndices dos vizinhos no DataFrame e a dist�ncia euclidiana at� cada um deles.

---

### `def acquisition_rate(df, idx_current, radius, neighbors)`

* **Prop�sito:** Calcula a taxa m�xima de aquisi��o de conhecimento para um indiv�duo Suscet�vel (S) ou Esquecedor (R).
* **Rela��o com o Artigo:**
    * [cite_start]**Taxa de Aquisi��o de Conhecimento:** Implementa a f�rmula da taxa de aquisi��o de conhecimento (Equa��o 4, Se��o 3.3.4)[cite: 2690, 2692]. [cite_start]O c�lculo considera a `learningCapability` do indiv�duo atual, a `transferCapability` de seus vizinhos Disseminadores (status 2) e a `dist�ncia celular` entre eles[cite: 2676, 2693].
    * [cite_start]**Estrat�gia de Troca:** A fun��o busca a taxa *m�xima* entre todos os vizinhos disseminadores, conforme especificado pela fun��o `max` na Equa��o 4, refletindo uma estrat�gia racional de aprendizado[cite: 2691].
* **Par�metros:**
    * `df`: O DataFrame da popula��o.
    * `idx_current`: O �ndice do indiv�duo cuja taxa est� sendo calculada.
    * `radius`, `neighbors`: Par�metros para definir a vizinhan�a.
* **Retorno:** Um valor `float` que representa a m�xima probabilidade de aquisi��o de conhecimento para o indiv�duo.

---

### `def transition_F(df, radius, neighbors)`

* [cite_start]**Prop�sito:** Esta � a fun��o central do aut�mato celular, que aplica as regras de transi��o para atualizar o estado de cada indiv�duo a cada ciclo de tempo[cite: 2612].
* **Rela��o com o Artigo:**
    * [cite_start]**Fun��o de Transi��o (F):** Representa a implementa��o completa das regras de transi��o de estado descritas na Se��o 3.3.4 e 3.3.5, e visualizadas na Figura 1[cite: 2603].
    * **Transi��es de Estado:**
        1.  [cite_start]**S ? E** e **R ? E:** Utiliza a `acquisition_rate()` e um sorteio aleat�rio para determinar se um Suscet�vel ou Esquecedor se torna um Contatante[cite: 2605, 2609].
        2.  [cite_start]**E ? {I, R, Q}:** Para um Contatante, calcula as taxas de absor��o (`Il`), esquecimento (`Rl`) e desist�ncia (`Ql`) ajustadas pelo n�mero de vezes que o indiv�duo j� foi contatante (`D`), conforme as f�rmulas $R'_L = R_L^{(D+1)}$ e $Q'_L = Q_L^{(D+1)}$ (Se��o 3.3.5)[cite: 2707, 2712]. Um sorteio aleat�rio decide o pr�ximo estado.
* **Par�metros:**
    * `df`: O DataFrame da popula��o no estado atual.
    * `radius`, `neighbors`: Par�metros da vizinhan�a.
* **Retorno:** Um novo DataFrame com os status dos indiv�duos atualizados para o pr�ximo ciclo de tempo.

---

### `def simular_difusao(df, MD=20, IM=50, radius=1, neighbors='Moore', press=False)`

* **Prop�sito:** Orquestra a simula��o completa, executando o loop principal por um n�mero definido de ciclos (itera��es).
* **Rela��o com o Artigo:**
    * [cite_start]**Processo de Simula��o:** Executa a simula��o por 50 "semanas" (ciclos), conforme mencionado na Se��o 4.1[cite: 2735]. Em cada ciclo, aplica primeiro a fun��o de transi��o (`transition_F`) e depois a fun��o de mobilidade (`mobility`), seguindo a l�gica do modelo de AC aprimorado.
* **Par�metros:**
    * `df`: O DataFrame da configura��o inicial.
    * Todos os outros par�metros (`MD`, `IM`, `radius`, etc.) s�o passados para as fun��es internas.
* **Retorno:** Um DataFrame contendo o hist�rico das estat�sticas (contagem de indiv�duos em cada estado) para cada ciclo da simula��o.

---

### `def plot_results(...)` e `run_experiment_figure_X(...)`

* **Prop�sito:**
    * `plot_results`: Uma fun��o gen�rica para visualizar os resultados das simula��es, criando gr�ficos que replicam o estilo dos apresentados no artigo.
    * `run_experiment_figure_X`: Fun��es espec�ficas (`run_experiment_figure_4`, `run_experiment_figure_6`, etc.) que configuram e executam as simula��es para replicar cada um dos experimentos e figuras do artigo (Figuras 4 a 8).
* **Rela��o com o Artigo:**
    * [cite_start]**M�tricas de Desempenho:** A fun��o `plot_results` calcula e plota as duas m�tricas de avalia��o definidas na Se��o 4.1: a propor��o de disseminadores ($r_t$, Equa��o 5) e a velocidade de difus�o ($v_t$, Equa��o 6)[cite: 2736, 2737, 2739].
    * [cite_start]**Replica��o dos Experimentos:** As fun��es `run_experiment_...` automatizam a execu��o de m�ltiplas rodadas para cada cen�rio experimental (50 vezes, conforme Se��o 4.1), calculando a m�dia dos resultados para garantir robustez estat�stica, uma pr�tica padr�o em estudos de simula��o[cite: 2735].
* **Par�metros:** Variam de acordo com o experimento, ajustando `distribution_type`, `radius`, `neighbors`, `MD`, `IM` e o intervalo das taxas de desist�ncia para corresponder �s condi��es de cada figura do artigo.
* **Retorno:** Nenhuma. As fun��es salvam os gr�ficos gerados em arquivos de imagem.
