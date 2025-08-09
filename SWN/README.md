# 2- Projeto: Implementação da Simulação de Difusão de Conhecimento com Redes de Pequeno Mundo (Small Wold Networks-SWN)

## Introdução

Este projeto (SWN_KCO.ipynb) é uma **adaptação** do modelo de simulação apresentado no artigo *"Modelling and simulating knowledge diffusion in knowledge collaboration organisations using improved cellular automata"*.

Diferente da implementação original que utiliza um autômato celular em um grid 2D, este código modela a organização (KCO) como uma **Rede de Pequeno Mundo (Small-World Network)**, gerada pelo algoritmo de Watts-Strogatz. Esta abordagem, que utiliza a biblioteca do python `networkx`, permite explorar como uma topologia de rede mais complexa e realista, caracterizada por alta clusterização local e "atalhos" de longa distância, afeta a dinâmica da difusão de conhecimento.

O objetivo é investigar se os padrões de difusão observados no modelo de grade se mantêm ou se alteram em uma estrutura de rede que se assemelha mais a redes sociais e de colaboração reais.

## Estrutura do Código

O código segue uma estrutura lógica similar à da implementação original, mas adaptada para operar sobre uma estrutura de grafo:

1.  **Criação do Grafo:** Geração da rede e atribuição de atributos aos nós.
2.  **Dinâmica da Rede:** Implementação das regras de transição de estado e mobilidade.
3.  **Simulação e Análise:** Execução dos experimentos e visualização dos resultados.

## Descrição Detalhada das Funções

A seguir, cada função do código é explicada, com foco nas adaptações feitas para o modelo de rede.

---
### `def set_up_configuration(n_cells=400, k_neighbors=8, p_rewire=0.1, ...)`

* **Propósito:** Inicializa a simulação criando uma Rede de Pequeno Mundo e configurando os atributos de cada indivíduo (nó).
* **Adaptação do Artigo:**
    * **Topologia da Rede:** Em vez de um grid, a estrutura da organização é criada usando `nx.watts_strogatz_graph`. Esta função gera uma rede que possui alta clusterização local (como em grupos de trabalho) e atalhos de longa distância (conexões entre diferentes grupos), uma característica central das redes de pequeno mundo.
    * **Parâmetros da Rede:**
        * `n_cells`: O número de nós no grafo (total de indivíduos).
        * `k_neighbors`: O número de vizinhos com os quais cada nó é inicialmente conectado em uma estrutura de anel. Este parâmetro controla a densidade de conexões locais.
        * `p_rewire`: A probabilidade de religar cada aresta para criar atalhos. Um `p_rewire=0` resulta em uma rede regular (alta clusterização, sem atalhos), enquanto `p_rewire=1` gera uma rede aleatória.
    * **Distribuição Inicial:** A lógica para definir os disseminadores iniciais (`random`, `monopolistic`, `small-group`) foi adaptada para o grafo, selecionando nós com base em sua posição na rede (ex: um nó central e seus vizinhos para `monopolistic`) com parâmetro de religação 0 (`p_rewire=0`).
* **Retorno:** Um objeto de grafo (`networkx.Graph`) onde cada nó possui os atributos definidos no artigo (status, capacidades, taxas, etc.).

---
### `def plot_initial_graph()`

* **Propósito:** Visualiza a configuração inicial do grafo.
* **Adaptação do Artigo:** Como a rede não tem uma posição espacial fixa como um grid, a função utiliza um algoritmo de layout (`nx.kamada_kawai_layout`) para posicionar os nós de forma esteticamente organizada. As cores dos nós representam seu estado inicial (Suscetível ou Disseminador).

---
### `def acquisition_rate(G, node_id)`

* **Propósito:** Calcula a taxa de aquisição de conhecimento para um nó específico.
* **Adaptação do Artigo:** Esta é uma das adaptações mais importantes. No modelo de rede, a interação ocorre apenas entre **vizinhos diretos**.
    * **Vizinhança:** A busca por disseminadores é feita com `G.neighbors(node_id)`.
    * **Distância Celular:** O conceito de distância euclidiana do modelo em grade é substituído pela existência de uma conexão direta. A fórmula de aquisição (Equação 4) é simplificada, removendo o termo `1/dist`, pois a "distância" para um vizinho é efetivamente 1. A força da interação agora depende apenas das capacidades de aprendizado e transferência.

---
### `def transition_F(G)`

* **Propósito:** Aplica as regras de transição de estado para todos os nós no grafo, simulando a evolução do conhecimento em um ciclo de tempo.
* **Adaptação do Artigo:** A lógica desta função é **quase idêntica** à do modelo original. As transições de estado (S→E, E→{I,R,Q}, R→E) dependem dos atributos individuais de cada nó e das interações com seus vizinhos (via `acquisition_rate`), um processo que se aplica igualmente bem a uma estrutura de grafo. O reforço de aprendizado e as probabilidades de transição são calculados da mesma forma que no artigo original.

---
### `def mobility(G, IM=0, MD=0, ...)`

* **Propósito:** Simula a mobilidade dos indivíduos, permitindo que eles troquem de "posição" na estrutura da rede.
* **Adaptação do Artigo:** A implementação da mobilidade em um grafo é significativamente mais complexa do que em um grid. Enquanto no grid apenas os atributos eram trocados, aqui a função simula uma troca completa de papéis na rede:
    1.  **Troca de Atributos:** Os atributos (status, capacidades, etc.) de dois nós selecionados são trocados.
    2.  **Religação da Rede:** As conexões dos dois nós são removidas e, em seguida, recriadas em suas novas posições. O nó `n1` passa a ter as conexões que o nó `n2` tinha, e vice-versa.
    * Isso simula a ideia de um indivíduo se "mudando" para o lugar de outro na estrutura organizacional, herdando seu círculo de colaborações.

---
### `def simular_difusao(G_initial, MD=0, IM=0, max_iter=50)`

* **Propósito:** Executa o loop principal da simulação por 50 ciclos.
* **Adaptação do Artigo:** Orquestra a simulação chamando `transition_F` e, opcionalmente, `mobility` em cada passo. A principal diferença conceitual é que a própria estrutura da SWN, com seus atalhos (`p_rewire > 0`), já fornece um mecanismo de difusão de longa distância, que emula um dos efeitos da mobilidade no modelo de grade. A função `mobility` implementa um mecanismo adicional de mudança estrutural dinâmica.

---
### `def plot_results(...)` e `run_experiment_figure_X(...)`

* **Propósito:** Executar os experimentos descritos no artigo e visualizar os resultados.
* **Adaptação do Artigo:**
    * Estas funções foram adaptadas para usar os parâmetros do modelo SWN (`k_neighbors`, `p_rewire`).
    * **Métricas de Desempenho:** A função `plot_results` calcula e plota as duas métricas de avaliação definidas na Seção 4.1 do artigo: a proporção de disseminadores ($r_t$, Equação 5) e a velocidade de difusão ($v_t$, Equação 6).
    * **Replicação dos Experimentos:** As funções `run_experiment_...` automatizam a execução de múltiplas rodadas para cada cenário experimental (50 vezes, conforme Seção 4.1), calculando a média dos resultados para garantir robustez estatística.
    * **Novo Experimento (Figura 9):** Foi adicionada a função `run_experiment_figure_9`, que realiza um novo experimento para analisar o impacto do parâmetro `p_rewire` na difusão. Este é um teste exclusivo para o modelo de Rede de Pequeno Mundo, investigando como a quantidade de "atalhos" na rede influencia a velocidade e o alcance da disseminação do conhecimento.
    * **Retorno:** Nenhuma. As funções salvam os gráficos gerados em arquivos de imagem com os nomes: figura_4_simulacao_swn.png, figura_5_simulacao_swn.png, figura_6_simulacao_swn.png, figura_7_simulacao_swn.png, figura_8_simulacao_swn.png e figura_9_simulacao_swn.png.

---
## Parte 2: Adaptação com Religação Dinâmica

Esta seção descreve uma abordagem alternativa para modelar a dinâmica da rede, substituindo a função `mobility` por uma **religação dinâmica** que ocorre durante a simulação.

### `def religacao_dinamica(G, p_rewire, IM=0)`

* **Propósito:** Modifica dinamicamente a topologia da rede a cada ciclo, simulando a evolução das relações de colaboração ao longo do tempo.
* **Relação com o Artigo (e Adaptação):** Esta função oferece uma nova interpretação para a **"mobilidade individual"** (Seção 3.3.6). Enquanto a mobilidade no artigo implica a troca de posições de indivíduos em um espaço fixo, a religação dinâmica modela a **"mobilidade social"**:
    * Em vez de trocar os indivíduos de lugar, a função altera com quem eles se conectam. Isso representa a formação e o desfazimento de laços de colaboração, que é um processo comum em KCOs.
    * O parâmetro `p_rewire` aqui controla a probabilidade de um nó alterar uma de suas conexões em um determinado passo de tempo.
    * O parâmetro `IM` define a porcentagem de nós que são considerados para a religação em cada ciclo.
* **Implementação:**
    1.  Uma proporção (`IM`) de nós é considerada para a religação.
    2.  Para cada nó, com uma probabilidade `p_rewire`, uma de suas conexões existentes é aleatoriamente **removida**.
    3.  Uma **nova conexão** é então estabelecida com outro nó da rede escolhido aleatoriamente, com a condição de que ele não seja o próprio nó ou um de seus vizinhos já existentes.

---
### `def simular_difusao2(G_initial, IM=0, p_rewire=0.1, max_iter=50)`

* **Propósito:** Orquestra a simulação utilizando o novo mecanismo de religação dinâmica.
* **Adaptação:** Esta função substitui a chamada à função `mobility` pela nova `religacao_dinamica` dentro do loop da simulação. A ordem das operações em cada ciclo é:
    1.  **Difusão do Conhecimento:** A função `transition_F` é chamada, permitindo que o conhecimento se espalhe pela rede em seu estado atual.
    2.  **Evolução da Rede:** A função `religacao_dinamica` é chamada para modificar a topologia da rede.
    * Este processo simula um ciclo realista onde as colaborações atuais influenciam a difusão, e em seguida, a própria estrutura de colaboração evolui para o próximo ciclo.
