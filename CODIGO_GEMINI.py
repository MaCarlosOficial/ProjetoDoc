import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt

# --- PARÂMETROS GLOBAIS ---
rows, cols = 20, 20
n_cells = rows * cols

# --- FUNÇÕES DE SETUP E SIMULAÇÃO ---

def setup_initial_distribution(distribution_type='random', min_rate=0.0, max_rate=0.25):
    """
    Cria o DataFrame inicial com diferentes distribuições e taxas.
    """
    rows_grid, cols_grid = np.mgrid[0:rows, 0:cols]
    row_indices, col_indices = rows_grid.flatten(), cols_grid.flatten()
    pop_status = np.zeros(n_cells, dtype=int)
    num_disseminators = n_cells * 5 // 100

    if distribution_type == 'monopolistic':
        center_r, center_c = rows // 2, cols // 2
        count = 0
        for r_offset in range(-2, 3):
            for c_offset in range(-2, 3):
                if count < num_disseminators and -1 < (center_r + r_offset) < rows and -1 < (center_c + c_offset) < cols:
                    idx = (center_r + r_offset) * cols + (center_c + c_offset)
                    pop_status[idx] = 2
                    count += 1
    elif distribution_type == 'small-group':
        coords = [(3, 3), (3, 16), (16, 3), (16, 16)]
        count = 0
        for gr, gc in coords:
            for r_offset in range(3):
                for c_offset in range(3):
                     if count < num_disseminators:
                        idx = (gr + r_offset) * cols + (gc + c_offset)
                        if idx < len(pop_status) and pop_status[idx] == 0:
                            pop_status[idx] = 2
                            count += 1
    else: # 'random'
        pop_status[:num_disseminators] = 2
        np.random.shuffle(pop_status)

    data = {
        'row': row_indices, 'col' : col_indices, 'status': pop_status,
        'learningCapability': np.abs(np.random.normal(loc=0.5, scale=0.2, size=n_cells)),
        'transferCapability': np.abs(np.random.normal(loc=0.5, scale=0.2, size=n_cells)),
        'forgettingRate': np.random.uniform(min_rate, max_rate, n_cells),
        'quittingRate': np.random.uniform(min_rate, max_rate, n_cells),
        'timesContactor': np.zeros(n_cells, dtype=int)
    }
    return pd.DataFrame(data)

def mobility(df, MD_param, IM_percent):
    if MD_param == 0 or IM_percent == 0: return df
    new_df = df.copy()
    num_individuals = len(new_df)
    columns_to_swap = [col for col in new_df.columns if col not in ['row', 'col']]
    num_to_move = (num_individuals * IM_percent) // 100
    indices_to_move = np.random.choice(df.index, size=num_to_move, replace=False)
    for idx1_df in indices_to_move:
        row1, col1 = new_df.loc[idx1_df, ['row', 'col']]
        md_r, md_c = np.random.randint(-MD_param, MD_param + 1), np.random.randint(-MD_param, MD_param + 1)
        if md_r == 0 and md_c == 0: continue
        row2, col2 = (row1 + md_r) % rows, (col1 + md_c) % cols
        idx2_series = new_df[(new_df['row'] == row2) & (new_df['col'] == col2)].index
        if not idx2_series.empty:
            idx2_df = idx2_series[0]
            if idx1_df == idx2_df: continue
            temp_attributes = new_df.loc[idx1_df, columns_to_swap].copy()
            new_df.loc[idx1_df, columns_to_swap] = new_df.loc[idx2_df, columns_to_swap]
            new_df.loc[idx2_df, columns_to_swap] = temp_attributes
    return new_df

def neighbors(df, point, radius, neighbors_type):
    current_row, current_col = point
    neighbor_info = []
    for dr in range(-radius, radius + 1):
        for dc in range(-radius, radius + 1):
            if dr == 0 and dc == 0: continue
            include_neighbor = False
            if neighbors_type == "Moore" and max(abs(dr), abs(dc)) <= radius:
                include_neighbor = True
            elif neighbors_type == "VonNeumann" and abs(dr) + abs(dc) <= radius:
                include_neighbor = True
            if include_neighbor:
                neighbor_row, neighbor_col = (current_row + dr) % rows, (current_col + dc) % cols
                idx_neighbor_series = df[(df['row'] == neighbor_row) & (df['col'] == neighbor_col)].index
                if not idx_neighbor_series.empty:
                    idx_neighbor = idx_neighbor_series[0]
                    euclidean_dist = math.sqrt(dr**2 + dc**2)
                    if euclidean_dist > 0:
                        neighbor_info.append([idx_neighbor, euclidean_dist])
    return neighbor_info

def calculate_max_acquisition_rate(df, lc_agent, current_point_coords, radius_param, neighbors_type_param):
    neighbor_data = neighbors(df, current_point_coords, radius=radius_param, neighbors_type=neighbors_type_param)
    max_rate = 0.0
    for idx_neighbor, dist_euclidean in neighbor_data:
        status_neighbor = df.loc[idx_neighbor, 'status']
        if status_neighbor == 2:
            tc_neighbor_I = df.loc[idx_neighbor, 'transferCapability']
            product_of_caps = lc_agent * tc_neighbor_I
            if product_of_caps < 0: product_of_caps = 0
            current_rate = (1 / dist_euclidean) * math.sqrt(product_of_caps)
            if current_rate > max_rate: max_rate = current_rate
    return max_rate

def transition_F(df, radius_param, neighbors_type_param):
    df_initial_state = df.copy()
    for idx in df.index:
        status, D = df_initial_state.loc[idx, ['status', 'timesContactor']]
        if status == 0: # S -> E
            coords = (df_initial_state.loc[idx, 'row'], df_initial_state.loc[idx, 'col'])
            lc_S = df_initial_state.loc[idx, 'learningCapability']
            rate = calculate_max_acquisition_rate(df_initial_state, lc_S, coords, radius_param, neighbors_type_param)
            if rate > 0 and np.random.random() < np.clip(rate, 0, 1):
                df.at[idx, 'status'], df.at[idx, 'timesContactor'] = 1, D + 1
        elif status == 1: # E -> I, R, Q
            txR, txQ = df_initial_state.loc[idx, ['forgettingRate', 'quittingRate']]
            exp = D + 1
            Rl, Ql = np.clip(txR ** exp, 0, 1), np.clip(txQ ** exp, 0, 1)
            Il = 1.0 - Rl - Ql
            if Il < 0:
                Il = 0
                if (Rl + Ql) > 1e-9: Rl, Ql = Rl / (Rl + Ql), Ql / (Rl + Ql)
            rand_val = np.random.rand()
            if rand_val < Ql: df.at[idx, 'status'] = 4
            elif rand_val < (Ql + Rl): df.at[idx, 'status'] = 3
            else: df.at[idx, 'status'] = 2
        elif status == 3: # R -> E
            coords = (df_initial_state.loc[idx, 'row'], df_initial_state.loc[idx, 'col'])
            base_lc_R = df_initial_state.loc[idx, 'learningCapability']
            lc_R_for_attempt = base_lc_R ** (1.0 / (D + 1.0)) if base_lc_R > 0 and D >= 0 else 0.0
            rate = calculate_max_acquisition_rate(df_initial_state, lc_R_for_attempt, coords, radius_param, neighbors_type_param)
            if rate > 0 and np.random.random() < np.clip(rate, 0, 1):
                df.at[idx, 'status'], df.at[idx, 'timesContactor'] = 1, D + 1
    return df

def simular_difusao(df_param, max_iter=50, md_sim=0, im_sim=0, radius_sim=1, neighbors_type_sim='Moore'):
    df_current = df_param.copy()
    history_stats = []
    initial_counts = df_current['status'].value_counts().to_dict()
    initial_state = {'ciclo': 0, **{f'status_{s}': initial_counts.get(s, 0) for s in range(5)}}
    history_stats.append(initial_state)
    for passo in range(1, max_iter + 1):
        df_current = transition_F(df_current, radius_param=radius_sim, neighbors_type_param=neighbors_type_sim)
        df_current = mobility(df_current, MD_param=md_sim, IM_percent=im_sim)
        status_counts = df_current['status'].value_counts().to_dict()
        current_stats = {'ciclo': passo, **{f'status_{s}': status_counts.get(s, 0) for s in range(5)}}
        history_stats.append(current_stats)
    return history_stats

def plot_results(results_dict, title_prefix, filename, colors=None, linestyles=None, markers=None):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    for name, df_history in results_dict.items():
        df_history['r_t'] = df_history['status_2'] / n_cells
        df_history['v_t'] = df_history['status_2'].diff().fillna(0)
        ax1.plot(df_history['ciclo'], df_history['r_t'], label=name,
                 color=colors.get(name) if colors else None,
                 linestyle=linestyles.get(name) if linestyles else '-', marker='o', markersize=3)
        ax2.plot(df_history['ciclo'], df_history['v_t'], label=name,
                 color=colors.get(name) if colors else None,
                 linestyle=linestyles.get(name, '--') if linestyles else '--', marker='x', markersize=4)
    ax1.set_title('(a) Proporção de Disseminadores vs. Tempo')
    ax1.set_xlabel('Ciclos de Tempo')
    ax1.set_ylabel('Proporção de Disseminadores ($r_t$)')
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax1.legend()
    ax1.set_ylim(0, 1.05)
    ax1.set_xlim(0, 50)
    ax2.set_title('(b) Velocidade de Difusão vs. Tempo')
    ax2.set_xlabel('Ciclos de Tempo')
    ax2.set_ylabel('Novos Disseminadores ($v_t$)')
    ax2.grid(True, linestyle='--', alpha=0.6)
    ax2.legend()
    ax2.set_xlim(0, 50)
    fig.suptitle(title_prefix, fontsize=16)
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(filename, dpi=300)
    print(f"Gráficos salvos com sucesso no arquivo '{filename}'")
    plt.close(fig)

# --- FUNÇÕES DE EXECUÇÃO DOS EXPERIMENTOS ---

def run_experiment_figure_4():
    """Executa as simulações para replicar a Figura 4."""
    print("\n--- Iniciando simulações para a Figura 4: Impacto da Distribuição Inicial ---")
    scenarios = ['random', 'small-group', 'monopolistic']
    results = {}
    for scenario in scenarios:
        print(f"  Executando cenário: {scenario.capitalize()}...")
        np.random.seed(1)
        initial_grid = setup_initial_distribution(distribution_type=scenario)
        history = simular_difusao(initial_grid, max_iter=50, radius_sim=1, neighbors_type_sim='Moore')
        results[scenario.capitalize()] = pd.DataFrame(history)
    plot_results(results,
                 'Impacto da Distribuição Inicial dos Disseminadores',
                 'figura_4_simulacao.png',
                 colors={'Random': 'green', 'Small-group': 'orange', 'Monopolistic': 'blue'},
                 linestyles={'Random': '-', 'Small-group': '--', 'Monopolistic': ':'})

def run_experiment_figure_5():
    """Executa as simulações para replicar a Figura 5."""
    print("\n--- Iniciando simulações para a Figura 5: Impacto da Vizinhança ---")
    scenarios = {
        '1x1 Von Neumann': {'radius': 1, 'type': 'VonNeumann'},
        '1x1 Moore':       {'radius': 1, 'type': 'Moore'},
        '2x2 Von Neumann': {'radius': 2, 'type': 'VonNeumann'},
        '2x2 Moore':       {'radius': 2, 'type': 'Moore'}
    }
    results = {}
    np.random.seed(42)
    initial_grid = setup_initial_distribution(distribution_type='random')
    for name, params in scenarios.items():
        print(f"  Executando cenário: {name}...")
        history = simular_difusao(initial_grid.copy(), max_iter=50,
                                  radius_sim=params['radius'], neighbors_type_sim=params['type'])
        results[name] = pd.DataFrame(history)
    plot_results(results,
                 'Impacto da Acessibilidade ao Conhecimento (Vizinhança)',
                 'figura_5_simulacao.png')

def run_experiment_figure_6():
    """Executa as simulações para replicar a Figura 6 (Impacto da Proporção de Indivíduos Móveis)."""
    print("\n--- Iniciando simulações para a Figura 6: Impacto da Proporção de Móveis (IM) ---")
    scenarios = [0, 20, 50, 100]
    results = {}
    np.random.seed(43)
    initial_grid = setup_initial_distribution(distribution_type='random')
    for im_percent in scenarios:
        name = f'IM = {im_percent}%'
        print(f"  Executando cenário: {name}...")
        history = simular_difusao(initial_grid.copy(), max_iter=50,
                                  md_sim=5, im_sim=im_percent,
                                  radius_sim=1, neighbors_type_sim='VonNeumann')
        results[name] = pd.DataFrame(history)
    plot_results(results,
                 'Impacto da Proporção de Indivíduos Móveis (IM)',
                 'figura_6_simulacao.png')

def run_experiment_figure_7():
    """Executa as simulações para replicar a Figura 7 (Impacto da Distância Máxima de Movimento)."""
    print("\n--- Iniciando simulações para a Figura 7: Impacto da Distância de Movimento (MD) ---")
    scenarios = [0, 5, 10, 20]
    results = {}
    np.random.seed(44)
    initial_grid = setup_initial_distribution(distribution_type='random')
    for md_dist in scenarios:
        name = f'MD = {md_dist}'
        print(f"  Executando cenário: {name}...")
        history = simular_difusao(initial_grid.copy(), max_iter=50,
                                  md_sim=md_dist, im_sim=20,
                                  radius_sim=1, neighbors_type_sim='VonNeumann')
        results[name] = pd.DataFrame(history)
    plot_results(results,
                 'Impacto da Distância Máxima de Movimento (MD)',
                 'figura_7_simulacao.png')

def run_experiment_figure_8():
    """Executa as simulações para replicar a Figura 8 (Impacto da Taxa de Desistência)."""
    print("\n--- Iniciando simulações para a Figura 8: Impacto da Taxa de Desistência ---")
    # Interpretando a notação N(a,b) do artigo como uma distribuição Uniforme(a,b)
    scenarios = {
        'Taxa [0-0.25]':    {'min': 0.0, 'max': 0.25},
        'Taxa [0.25-0.5]':  {'min': 0.25, 'max': 0.50},
        'Taxa [0.5-0.75]':  {'min': 0.50, 'max': 0.75},
        'Taxa [0.75-1.0]':  {'min': 0.75, 'max': 1.0} # Corrigindo o provável typo do artigo N(0.75, 0.10)
    }
    results = {}
    for name, params in scenarios.items():
        print(f"  Executando cenário: {name}...")
        np.random.seed(45)
        initial_grid = setup_initial_distribution(distribution_type='random',
                                                min_rate=params['min'],
                                                max_rate=params['max'])
        history = simular_difusao(initial_grid.copy(), max_iter=50,
                                  radius_sim=1, neighbors_type_sim='Moore')
        results[name] = pd.DataFrame(history)
    plot_results(results,
                 'Impacto da Taxa de Desistência do Conhecimento',
                 'figura_8_simulacao.png')

# --- BLOCO PRINCIPAL DE EXECUÇÃO ---
if __name__ == "__main__":
    # Experimentos já implementados
    run_experiment_figure_4()
    run_experiment_figure_5()

    # Novos experimentos para as Figuras 6, 7 e 8
    run_experiment_figure_6()
    run_experiment_figure_7()
    run_experiment_figure_8()

    print("\nTodos os experimentos foram concluídos com sucesso.")