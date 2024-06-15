import random as random
from sklearn.metrics import mean_squared_error
import gurobipy as gp
import pandas as pd
import numpy as np

class AlgorithmDepolarize():
    
    def __init__(self, X, omega, axis):
        self.axis = axis
        self.omega = omega
        self.X = X.mask(~omega)
        self.omega_user = omega.sum(axis=axis)
    
    def evaluate(self, X_est, alpha = 0.8, h = 3):
        list_X_est = []
        for x in range(0, h):
            print("x: ", x)
            list_X_est.append(self.get_X_est_polarizacao(X_est.copy(), alpha))
        return list_X_est
        
    def get_differences_means(self, X_est):
        X = self.X
        X_est = X_est.mask(~self.omega)

        E = (X_est - X)
        losses = E.mean(axis=self.axis)
        return losses

    def get_differences_vars(self, X_est):
        X = self.X
        X_est = X_est.mask(~self.omega)
        E = (X_est - X).pow(2)
        losses = E.mean(axis=self.axis)
        return losses
        

    # Versão 01: Melhora a polarização
    def get_X_est_polarizacao(self, X_est, alpha = 0.8):
        # Calcular a média dos valores de X_est
        media_X_est = X_est.mean().mean()

        # Calcular o desvio de cada elemento em relação à média
        desvio = X_est - media_X_est
        
        # Definir a fração do desvio que será usada para ajustar os valores
        # Você pode ajustar essa fração conforme necessário
        # fracao_ajuste = 0.7
        # fracao_ajuste = 0.25
        fracao_ajuste = random.uniform(0, alpha)
        
        # Ajustar os valores de X_est para movê-los em direção à média
        X_est_adjusted = X_est - (desvio * fracao_ajuste)
        
        # Garantir que os valores ajustados estejam no intervalo [1, 5]
        X_est_adjusted = X_est_adjusted.clip(lower=1, upper=5)
        
        return X_est_adjusted
    

    def losses_to_ZIL(list_losses, n_items=1000):
        Z = []
        for losses in list_losses:
            linha = []
            for i in range(n_items):
                linha.append(losses.values[i])
            Z.append(linha)
        return Z
    
    def polarizations_to_ZIP(list_polarizations, n_items=1000):
        Z = []
        for polarizations in list_polarizations:
            linha = []
            for i in range(n_items):
                linha.append(polarizations.values[i])
            Z.append(linha)
        return Z

    def matrices_Zs(Z, G): # return a Z matrix for each group
        list_Zs = []
        for group in G: # G = {1: [1,2], 2: [3,4,5]}
            Z_ = []
            list_users = G[group]
            for user in list_users:
                Z_.append(Z[user].copy())   
            list_Zs.append(Z_)
        return list_Zs
    

    def make_matrix_X_pi_annealing(list_X_est, ZIL, ZIP, num_iterations=10000, initial_temp=1000, cooling_rate=0.995):
        # Normalizar ZIL e ZIP
        ZIL_array = np.array(ZIL)
        ZIP_array = np.array(ZIP)
        ZIL_min, ZIL_max = ZIL_array.min(), ZIL_array.max()
        ZIP_min, ZIP_max = ZIP_array.min(), ZIP_array.max()

        ZIL_normalized = (ZIL_array - ZIL_min) / (ZIL_max - ZIL_min) if ZIL_max > ZIL_min else ZIL_array - ZIL_min
        ZIP_normalized = (ZIP_array - ZIP_min) / (ZIP_max - ZIP_min) if ZIP_max > ZIP_min else ZIP_array - ZIP_min

        h_matrices = len(ZIL_normalized)
        m_items = len(ZIL_normalized[0])

        # Função para calcular Rpol e Rindv
        def calculate_objective(W):
            Rpol = np.mean(ZIP_normalized[W == 1])
            Rindv = np.var(ZIL_normalized[W == 1])
            return 0.01*Rpol + Rindv
            # return Rindv

        # Inicializar uma matriz W aleatória
        W = np.zeros((h_matrices, m_items), dtype=int)
        for j in range(m_items):
            row = np.random.randint(h_matrices)
            W[row, j] = 1

        best_W = np.copy(W)
        best_objective = calculate_objective(best_W)
        current_objective = best_objective
        temperature = initial_temp

        # Pré-converter os DataFrames de entrada para arrays numpy para operações mais rápidas
        list_X_est_np = [x.values for x in list_X_est]

        for _ in range(num_iterations):
            # Fazer uma pequena mudança em W (mover um único 1 para uma linha diferente)
            new_W = np.copy(W)
            col = np.random.randint(m_items)
            current_row = np.argmax(new_W[:, col])
            new_row = np.random.randint(h_matrices)
            while new_row == current_row:
                new_row = np.random.randint(h_matrices)
            new_W[current_row, col] = 0
            new_W[new_row, col] = 1

            new_objective = calculate_objective(new_W)
            delta_objective = new_objective - current_objective

            if delta_objective < 0 or np.exp(-delta_objective / temperature) > np.random.rand():
                W = np.copy(new_W)
                current_objective = new_objective

                if current_objective < best_objective:
                    best_W = np.copy(W)
                    best_objective = current_objective

            temperature *= cooling_rate

        # Construir a matrix_final correspondente à melhor solução encontrada
        selected_columns = []
        for i in range(m_items):
            selected_rows = [list_X_est_np[j][:, i].reshape(-1, 1) for j in range(h_matrices) if best_W[j, i] == 1]
            selected_columns.append(np.hstack(selected_rows))

        best_matrix_final = np.hstack(selected_columns)
        best_matrix_final_df = pd.DataFrame(best_matrix_final, columns=[f'I{i}' for i in range(m_items)])

        #return best_matrix_final_df, pd.DataFrame(best_W, columns=[f'I{i}' for i in range(m_items)])
        return best_matrix_final_df

