import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Função para ler o arquivo Excel e preparar os dados.
def ler_dados(arquivo):
    dados = pd.read_excel(arquivo, header=1, index_col=0)
    return dados

# Função para transformar valores inteiros em contínuos usando uma distribuição normal
def transformar_continuo_normal(valores, escala=0.25):
    valores_continuos = []
    for valor in valores:
        valor_continuo = np.random.normal(loc=valor, scale=escala)
        valor_continuo = np.clip(valor_continuo, 1, 5)  # Garante que os valores estejam entre 1 e 5
        valores_continuos.append(valor_continuo)
    return np.array(valores_continuos)

# Arquivos Excel
# arquivo1 = 'X_MovieLens-1M_RecSysALS-08.xlsx'
# arquivo2 = 'Xest_MovieLens-1M_RecSysALS-08.xlsx'
# arquivo3 = 'XestPi_MovieLens-1M_RecSysALS-08.xlsx'

arquivo1 = 'X_Goodbooks-10k_RecSysALS-08.xlsx'
arquivo2 = 'Xest_Goodbooks-10k_RecSysALS-08.xlsx'
arquivo3 = 'XestPi_Goodbooks-10k_RecSysALS-08.xlsx'

# Ler os dados
dados1 = ler_dados(arquivo1)
dados2 = ler_dados(arquivo2)
dados3 = ler_dados(arquivo3)

# Criar máscara para dados válidos do arquivo 1
mascara = np.isfinite(dados1.values)

# Aplicar máscara aos arquivos 2 e 3
valores1 = dados1.values[mascara].flatten()
valores2 = dados2.values[mascara].flatten()
valores3 = dados3.values[mascara].flatten()

# Transformar valores inteiros de valores1 em contínuos usando distribuição normal
valores1_continuos = transformar_continuo_normal(valores1, escala=0.5)

# Plotar os gráficos de densidade
plt.figure(figsize=(10, 6))
sns.kdeplot(valores1_continuos, color='blue', linestyle='-', label='Avaliações conhecidas', fill=True, alpha=0.05)
sns.kdeplot(valores2, color='red', linestyle='-', label='Avaliações estimadas (antes)', fill=True, alpha=0.05)
sns.kdeplot(valores3, color='green', linestyle='--', label='Avaliações estimadas (depois)', fill=True, alpha=0.05)

# Ajustando limites dos eixos, rótulos e título
plt.xlim(min(valores1_continuos.min(), valores2.min(), valores3.min()) - 1, max(valores1_continuos.max(), valores2.max(), valores3.max()) + 1)
plt.xlabel('Valores')
plt.ylabel('Densidade')
plt.title('Gráfico de Densidade Comparativo')
plt.legend()

# Mostrar o gráfico
plt.show()
