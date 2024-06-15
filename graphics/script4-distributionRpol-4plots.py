import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Função para ler o arquivo Excel e preparar os dados.
def ler_dados(arquivo):
    dados = pd.read_excel(arquivo, header=1, index_col=0)
    return dados

# Arquivos Excel
arquivo_movielens_alfa08_Xest = 'Xest_MovieLens-1M_RecSysALS-08.xlsx'
arquivo_movielens_alfa08_Xpi = 'XestPi_MovieLens-1M_RecSysALS-08.xlsx'

arquivo_goodbooks_alfa08_Xest = 'Xest_Goodbooks-10k_RecSysALS-08.xlsx'
arquivo_goodbooks_alfa08_Xpi = 'XestPi_Goodbooks-10k_RecSysALS-08.xlsx'

# Ler os dados
dados_movielens_alfa08_Xest = ler_dados(arquivo_movielens_alfa08_Xest)
dados_movielens_alfa08_Xpi = ler_dados(arquivo_movielens_alfa08_Xpi)

dados_goodbooks_alfa08_Xest = ler_dados(arquivo_goodbooks_alfa08_Xest)
dados_goodbooks_alfa08_Xpi = ler_dados(arquivo_goodbooks_alfa08_Xpi)

# Calcular a variância de cada coluna
polarizacoes_movielens_alfa08_Xest = dados_movielens_alfa08_Xest.var()
polarizacoes_movielens_alfa08_Xpi = dados_movielens_alfa08_Xpi.var()
polarizacoes_goodbooks_alfa08_Xest = dados_goodbooks_alfa08_Xest.var()
polarizacoes_goodbooks_alfa08_Xpi = dados_goodbooks_alfa08_Xpi.var()

# Calcular as médias das variâncias
media_movielens_alfa08_Xest = polarizacoes_movielens_alfa08_Xest.mean()
media_movielens_alfa08_Xpi = polarizacoes_movielens_alfa08_Xpi.mean()
media_goodbooks_alfa08_Xest = polarizacoes_goodbooks_alfa08_Xest.mean()
media_goodbooks_alfa08_Xpi = polarizacoes_goodbooks_alfa08_Xpi.mean()

# Criar a figura e os subplots
fig, axs = plt.subplots(1, 2, figsize=(18, 12))
fig.suptitle('Distribuição e Média das $\sigma^2$ ($R_{pol}$)')

# Subplot para MovieLens com α=0.8
sns.kdeplot(polarizacoes_movielens_alfa08_Xest, color='red', linestyle='-', 
            label=fr'$\mathcal{{R}}_{{pol}}$ (antes) = {media_movielens_alfa08_Xest:.2f}', 
            ax=axs[0], fill=True, alpha=0.05, zorder=1)

sns.kdeplot(polarizacoes_movielens_alfa08_Xpi, color='green', linestyle='-', 
            label=fr'$\mathcal{{R}}_{{pol}}$ (depois) = {media_movielens_alfa08_Xpi:.2f}', 
            ax=axs[0], fill=True, alpha=0.05, zorder=1)

axs[0].axvline(media_movielens_alfa08_Xest, color='red', linestyle='-', zorder=2)
axs[0].axvline(media_movielens_alfa08_Xpi, color='green', linestyle='--', zorder=2)
# axs[0].set_xlabel('Variância das avaliações por item')
axs[0].set_xlabel(r'Variância ($\sigma^2$) das avaliações por item')
axs[0].set_ylabel('Densidade')
axs[0].set_title('MovieLens-1M α=0.8')

# Subplot para GoodBooks com α=0.8
# sns.kdeplot(polarizacoes_goodbooks_alfa08_Xest, color='red', linestyle='-', 
#             label=fr'$\mathcal{{R}}_{{pol}}(X, \hat{{X}})$ (antes) = {media_goodbooks_alfa08_Xest:.2f}', 
#             ax=axs[1], fill=True, alpha=0.05, zorder=1)

# sns.kdeplot(polarizacoes_goodbooks_alfa08_Xpi, color='green', linestyle='--', 
#             label=fr'$\mathcal{{R}}_{{pol}}(X, \hat{{X}}_\pi)$ (depois) = {media_goodbooks_alfa08_Xpi:.2f}', 
#             ax=axs[1], fill=True, alpha=0.05, zorder=1)

sns.kdeplot(polarizacoes_goodbooks_alfa08_Xest, color='red', linestyle='-', 
            label=fr'$\mathcal{{R}}_{{pol}}$ (antes) = {media_goodbooks_alfa08_Xest:.2f}', 
            ax=axs[1], fill=True, alpha=0.05, zorder=1)

sns.kdeplot(polarizacoes_goodbooks_alfa08_Xpi, color='green', linestyle='-', 
            label=fr'$\mathcal{{R}}_{{pol}}$ (depois) = {media_goodbooks_alfa08_Xpi:.2f}', 
            ax=axs[1], fill=True, alpha=0.05, zorder=1)

axs[1].axvline(media_goodbooks_alfa08_Xest, color='red', linestyle='-', zorder=2)
axs[1].axvline(media_goodbooks_alfa08_Xpi, color='green', linestyle='--', zorder=2)
axs[1].set_xlabel(r'Variância ($\sigma^2$) das avaliações por item')

axs[1].set_ylabel('Densidade')
axs[1].set_title('GoodBooks-10k α=0.8')

# Adicionando o texto \hat{X} no centro do gráfico
# axs[1].text(0.082, 0.25, r'$\hat{X}$', color='green', fontsize=18, ha='center', va='center', transform=axs[1].transAxes)
# axs[1].text(0.66, 0.25, r'$X$', color='red', fontsize=18, ha='center', va='center', transform=axs[1].transAxes)

# Legendas
for ax in axs:
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels, frameon=True)

# Ajustar o layout e mostrar o gráfico
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
