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
arquivo_movielens_alfa02_X = 'X_MovieLens-1M_RecSysALS-02.xlsx'
arquivo_movielens_alfa02_Xest = 'Xest_MovieLens-1M_RecSysALS-02.xlsx'
arquivo_movielens_alfa02_Xpi = 'XestPi_MovieLens-1M_RecSysALS-02.xlsx'

arquivo_movielens_alfa08_X = 'X_MovieLens-1M_RecSysALS-08.xlsx'
arquivo_movielens_alfa08_Xest = 'Xest_MovieLens-1M_RecSysALS-08.xlsx'
arquivo_movielens_alfa08_Xpi = 'XestPi_MovieLens-1M_RecSysALS-08.xlsx'

arquivo_goodbooks_alfa02_X = 'X_Goodbooks-10k_RecSysALS-02.xlsx'
arquivo_goodbooks_alfa02_Xest = 'Xest_Goodbooks-10k_RecSysALS-02.xlsx'
arquivo_goodbooks_alfa02_Xpi = 'XestPi_Goodbooks-10k_RecSysALS-02.xlsx'

arquivo_goodbooks_alfa08_X = 'X_Goodbooks-10k_RecSysALS-08.xlsx'
arquivo_goodbooks_alfa08_Xest = 'Xest_Goodbooks-10k_RecSysALS-08.xlsx'
arquivo_goodbooks_alfa08_Xpi = 'XestPi_Goodbooks-10k_RecSysALS-08.xlsx'


# Ler os dados
dados_movielens_alfa02_X = ler_dados(arquivo_movielens_alfa02_X)
dados_movielens_alfa02_Xest = ler_dados(arquivo_movielens_alfa02_Xest)
dados_movielens_alfa02_Xpi = ler_dados(arquivo_movielens_alfa02_Xpi)

dados_movielens_alfa08_X = ler_dados(arquivo_movielens_alfa08_X)
dados_movielens_alfa08_Xest = ler_dados(arquivo_movielens_alfa08_Xest)
dados_movielens_alfa08_Xpi = ler_dados(arquivo_movielens_alfa08_Xpi)

dados_goodbooks_alfa02_X = ler_dados(arquivo_goodbooks_alfa02_X)
dados_goodbooks_alfa02_Xest = ler_dados(arquivo_goodbooks_alfa02_Xest)
dados_goodbooks_alfa02_Xpi = ler_dados(arquivo_goodbooks_alfa02_Xpi)

dados_goodbooks_alfa08_X = ler_dados(arquivo_goodbooks_alfa08_X)
dados_goodbooks_alfa08_Xest = ler_dados(arquivo_goodbooks_alfa08_Xest)
dados_goodbooks_alfa08_Xpi = ler_dados(arquivo_goodbooks_alfa08_Xpi)

# Criar máscara para dados válidos do arquivo 1
mascara_movielens = np.isfinite(dados_movielens_alfa08_X.values)
mascara_goodbooks = np.isfinite(dados_goodbooks_alfa08_X.values)

# Aplicar máscara aos arquivos 2 e 3
valores_movielens_alfa02_X = dados_movielens_alfa02_X.values[mascara_movielens].flatten()
valores_movielens_alfa02_Xest = dados_movielens_alfa02_Xest.values[mascara_movielens].flatten()
valores_movielens_alfa02_Xpi = dados_movielens_alfa02_Xpi.values[mascara_movielens].flatten()

valores_movielens_alfa08_X = dados_movielens_alfa08_X.values[mascara_movielens].flatten()
valores_movielens_alfa08_Xest = dados_movielens_alfa08_Xest.values[mascara_movielens].flatten()
valores_movielens_alfa08_Xpi = dados_movielens_alfa08_Xpi.values[mascara_movielens].flatten()

valores_goodbooks_alfa02_X = dados_goodbooks_alfa02_X.values[mascara_goodbooks].flatten()
valores_goodbooks_alfa02_Xest = dados_goodbooks_alfa02_Xest.values[mascara_goodbooks].flatten()
valores_goodbooks_alfa02_Xpi = dados_goodbooks_alfa02_Xpi.values[mascara_goodbooks].flatten()

valores_goodbooks_alfa08_X = dados_goodbooks_alfa08_X.values[mascara_goodbooks].flatten()
valores_goodbooks_alfa08_Xest = dados_goodbooks_alfa08_Xest.values[mascara_goodbooks].flatten()
valores_goodbooks_alfa08_Xpi = dados_goodbooks_alfa08_Xpi.values[mascara_goodbooks].flatten()

# Transformar valores inteiros em contínuos usando distribuição normal
valores_movielens_alfa02_X_continuos = transformar_continuo_normal(valores_movielens_alfa02_X, escala=0.5)
valores_movielens_alfa08_X_continuos = transformar_continuo_normal(valores_movielens_alfa08_X, escala=0.5)
valores_goodbooks_alfa02_X_continuos = transformar_continuo_normal(valores_goodbooks_alfa02_X, escala=0.5)
valores_goodbooks_alfa08_X_continuos = transformar_continuo_normal(valores_goodbooks_alfa08_X, escala=0.5)

# Criar a figura e os subplots
fig, axs = plt.subplots(2, 2, figsize=(18, 12))
fig.suptitle('Gráfico de Densidade Comparativo')

# Subplot para MovieLens com α=0.2
sns.kdeplot(valores_movielens_alfa02_X_continuos, color='blue', linestyle='-', label='Avaliações conhecidas', ax=axs[0, 0], fill=True, alpha=0.05)
sns.kdeplot(valores_movielens_alfa02_Xest, color='red', linestyle='-', label='Avaliações estimadas (antes)', ax=axs[0, 0], fill=True, alpha=0.05)
sns.kdeplot(valores_movielens_alfa02_Xpi, color='green', linestyle='--', label='Avaliações estimadas (depois)', ax=axs[0, 0], fill=True, alpha=0.05)
axs[0, 0].set_xlim(min(valores_movielens_alfa02_X_continuos.min(), valores_movielens_alfa02_Xest.min(), valores_movielens_alfa02_Xpi.min()) - 1, max(valores_movielens_alfa02_X_continuos.max(), valores_movielens_alfa02_Xest.max(), valores_movielens_alfa02_Xpi.max()) + 0.02)
axs[0, 0].set_xlabel('Avaliações')
axs[0, 0].set_ylabel('Densidade')
axs[0, 0].set_title('MovieLens-1M α=0.2')
axs[0, 0].legend(loc='upper left')

# Subplot para MovieLens com α=0.8
sns.kdeplot(valores_movielens_alfa08_X_continuos, color='blue', linestyle='-', label='Avaliações conhecidas', ax=axs[0, 1], fill=True, alpha=0.05)
sns.kdeplot(valores_movielens_alfa08_Xest, color='red', linestyle='-', label='Avaliações estimadas (antes)', ax=axs[0, 1], fill=True, alpha=0.05)
sns.kdeplot(valores_movielens_alfa08_Xpi, color='green', linestyle='--', label='Avaliações estimadas (depois)', ax=axs[0, 1], fill=True, alpha=0.05)
axs[0, 1].set_xlim(min(valores_movielens_alfa08_X_continuos.min(), valores_movielens_alfa08_Xest.min(), valores_movielens_alfa08_Xpi.min()) - 1, max(valores_movielens_alfa08_X_continuos.max(), valores_movielens_alfa08_Xest.max(), valores_movielens_alfa08_Xpi.max()) + 0.02)
axs[0, 1].set_xlabel('Avaliações')
axs[0, 1].set_ylabel('Densidade')
axs[0, 1].set_title('MovieLens-1M α=0.8')
axs[0, 1].legend(loc='upper left')

# Subplot para GoodBooks com α=0.2
sns.kdeplot(valores_goodbooks_alfa02_X_continuos, color='blue', linestyle='-', label='Avaliações conhecidas', ax=axs[1, 0], fill=True, alpha=0.05)
sns.kdeplot(valores_goodbooks_alfa02_Xest, color='red', linestyle='-', label='Avaliações estimadas (antes)', ax=axs[1, 0], fill=True, alpha=0.05)
sns.kdeplot(valores_goodbooks_alfa02_Xpi, color='green', linestyle='--', label='Avaliações estimadas (depois)', ax=axs[1, 0], fill=True, alpha=0.05)
axs[1, 0].set_xlim(min(valores_goodbooks_alfa02_X_continuos.min(), valores_goodbooks_alfa02_Xest.min(), valores_goodbooks_alfa02_Xpi.min()) - 1, max(valores_goodbooks_alfa02_X_continuos.max(), valores_goodbooks_alfa02_Xest.max(), valores_goodbooks_alfa02_Xpi.max()) + 0.02)
axs[1, 0].set_xlabel('Avaliações')
axs[1, 0].set_ylabel('Densidade')
axs[1, 0].set_title('GoodBooks-10k α=0.2')
axs[1, 0].legend(loc='upper left')

# Subplot para GoodBooks com α=0.8
sns.kdeplot(valores_goodbooks_alfa08_X_continuos, color='blue', linestyle='-', label='Avaliações conhecidas', ax=axs[1, 1], fill=True, alpha=0.05)
sns.kdeplot(valores_goodbooks_alfa08_Xest, color='red', linestyle='-', label='Avaliações estimadas (antes)', ax=axs[1, 1], fill=True, alpha=0.05)
sns.kdeplot(valores_goodbooks_alfa08_Xpi, color='green', linestyle='--', label='Avaliações estimadas (depois)', ax=axs[1, 1], fill=True, alpha=0.05)
axs[1, 1].set_xlim(min(valores_goodbooks_alfa08_X_continuos.min(), valores_goodbooks_alfa08_Xest.min(), valores_goodbooks_alfa08_Xpi.min()) - 1, max(valores_goodbooks_alfa08_X_continuos.max(), valores_goodbooks_alfa08_Xest.max(), valores_goodbooks_alfa08_Xpi.max()) + 0.02)
axs[1, 1].set_xlabel('Avaliações')
axs[1, 1].set_ylabel('Densidade')
axs[1, 1].set_title('GoodBooks-10k α=0.8')
axs[1, 1].legend(loc='upper left')

# Ajustar o layout e mostrar o gráfico
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
