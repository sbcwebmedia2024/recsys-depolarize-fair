import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

class IndividualLossVariance():
    
    def __init__(self, X, omega, axis):
        self.axis = axis
        self.omega = omega
        self.X = X.mask(~omega)
        self.omega_user = omega.sum(axis=axis)
        
    def get_losses(self, X_est):
        X = self.X
        X_est = X_est.mask(~self.omega)
        E = (X_est - X).pow(2)
        losses = E.mean(axis=self.axis)
        return losses
        
    def evaluate(self, X_est):
        losses = self.get_losses(X_est)
        var =  losses.values.var()
        return var

    def gradient(self, X_est):
        """
        Returns the gradient of the utility.
        The output is an n by d matrix which is flatten.
        """
        X = self.X
        X_est = X_est.mask(~self.omega)
        diff = X_est - X
        if self.axis == 0:
            diff = diff.T
            
        losses = self.get_losses(X_est)
        B = losses - losses.mean()
        C = B.divide(self.omega_user)
        D = diff.multiply(C,axis=0)
        G = D.fillna(0).values
        if self.axis == 0:
            G = G.T
        return  G

# Função para ler o arquivo Excel e preparar os dados.
def ler_dados(arquivo):
    dados = pd.read_excel(arquivo, header=0, index_col=0)
    return dados

# Arquivos Excel
arquivo_movielens_alfa08_X = 'X_MovieLens-1M_RecSysALS-08.xlsx'
arquivo_movielens_alfa08_Xest = 'Xest_MovieLens-1M_RecSysALS-08.xlsx'
arquivo_movielens_alfa08_Xpi = 'XestPi_MovieLens-1M_RecSysALS-08.xlsx'

arquivo_goodbooks_alfa08_X = 'X_Goodbooks-10k_RecSysALS-08.xlsx'
arquivo_goodbooks_alfa08_Xest = 'Xest_Goodbooks-10k_RecSysALS-08.xlsx'
arquivo_goodbooks_alfa08_Xpi = 'XestPi_Goodbooks-10k_RecSysALS-08.xlsx'

# Ler os dados
dados_movielens_alfa08_X = ler_dados(arquivo_movielens_alfa08_X)
dados_movielens_alfa08_Xest = ler_dados(arquivo_movielens_alfa08_Xest)
dados_movielens_alfa08_Xpi = ler_dados(arquivo_movielens_alfa08_Xpi)

dados_goodbooks_alfa08_X = ler_dados(arquivo_goodbooks_alfa08_X)
dados_goodbooks_alfa08_Xest = ler_dados(arquivo_goodbooks_alfa08_Xest)
dados_goodbooks_alfa08_Xpi = ler_dados(arquivo_goodbooks_alfa08_Xpi)

# Criar máscara para dados válidos
mascara_movielens_alfa08 = ~dados_movielens_alfa08_X.isnull()
mascara_goodbooks_alfa08 = ~dados_goodbooks_alfa08_X.isnull()

ilv_movielens_alfa08_Xest = IndividualLossVariance(dados_movielens_alfa08_X, mascara_movielens_alfa08, 0)
losses_movielens_alfa08_Xest = ilv_movielens_alfa08_Xest.get_losses(dados_movielens_alfa08_Xest)
ilv_movielens_alfa08_Xpi = IndividualLossVariance(dados_movielens_alfa08_X, mascara_movielens_alfa08, 0)
losses_movielens_alfa08_Xpi = ilv_movielens_alfa08_Xpi.get_losses(dados_movielens_alfa08_Xpi)

ilv_goodbooks_alfa08_Xest = IndividualLossVariance(dados_goodbooks_alfa08_X, mascara_goodbooks_alfa08, 0)
losses_goodbooks_alfa08_Xest = ilv_goodbooks_alfa08_Xest.get_losses(dados_goodbooks_alfa08_Xest)
ilv_goodbooks_alfa08_Xpi = IndividualLossVariance(dados_goodbooks_alfa08_X, mascara_goodbooks_alfa08, 0)
losses_goodbooks_alfa08_Xpi = ilv_goodbooks_alfa08_Xpi.get_losses(dados_goodbooks_alfa08_Xpi)


# Calcular as médias das variâncias
media_movielens_alfa08_Xest = losses_movielens_alfa08_Xest.mean()
media_movielens_alfa08_Xpi = losses_movielens_alfa08_Xpi.mean()
media_goodbooks_alfa08_Xest = losses_goodbooks_alfa08_Xest.mean()
media_goodbooks_alfa08_Xpi = losses_goodbooks_alfa08_Xpi.mean()


# Calcular a variância das variâncias (Rindv)
variancia_movielens_alfa08_Xest = losses_movielens_alfa08_Xest.var()
variancia_movielens_alfa08_Xpi = losses_movielens_alfa08_Xpi.var()
variancia_goodbooks_alfa08_Xest = losses_goodbooks_alfa08_Xest.var()
variancia_goodbooks_alfa08_Xpi = losses_goodbooks_alfa08_Xpi.var()

# plt.title(r'Boxplot da Vari\^{a}ncia das Perdas dos Itens: Injusti\c{c}a Individual ($R_{indv}$)')

# Criar a figura e os subplots
fig, axs = plt.subplots(1, 2, figsize=(18, 12))
fig.suptitle('Boxplot da Variância das Perdas dos Itens')

# Subplot para MovieLens com α=0.8
sns.boxplot(data=[losses_movielens_alfa08_Xest, losses_movielens_alfa08_Xpi], notch=True, width=0.3, palette=['red', 'green'], ax=axs[0], flierprops=dict(marker='o', markerfacecolor='none', markersize=8))

axs[0].set_xticklabels(['Antes', 'Depois'])
axs[0].set_xlabel('Estado')
axs[0].set_ylabel('Perdas individuais por item ($\u2113$)')
axs[0].set_title('MovieLens-1M α=0.8')

# Subplot para GoodBooks com α=0.8
sns.boxplot(data=[losses_goodbooks_alfa08_Xest, losses_goodbooks_alfa08_Xpi], notch=True, width=0.3, palette=['red', 'green'], ax=axs[1], flierprops=dict(marker='o', markerfacecolor='none', markersize=8))

axs[1].set_xticklabels(['Antes', 'Depois'])
axs[1].set_xlabel('Estado')
axs[1].set_ylabel('Perdas individuais por item ($\u2113$)')
axs[1].set_title('GoodBooks-10k α=0.8')


legend_colors = ['red', 'green']  # Cores correspondentes aos boxplots

for i, ax in enumerate(axs):
    handles = [plt.Line2D([0], [0], marker='o', color='w', label=f'Color {i}', markerfacecolor=legend_colors[i], markersize=10) for i in range(2)]
    
    legend_labels = [f'$R_{{indv}}$ (antes): {variancia_movielens_alfa08_Xest:.2f}' if i == 0 else f'$R_{{indv}}$ (antes): {variancia_goodbooks_alfa08_Xest:.2f}',
                     f'$R_{{indv}}$ (depois):: {variancia_movielens_alfa08_Xpi:.2f}' if i == 0 else f'$R_{{indv}}$ (depois): {variancia_goodbooks_alfa08_Xpi:.2f}']

    ax.legend(handles, legend_labels, loc='upper center', frameon=True)

    ax.grid(axis='y')  # Adicionar linhas de grade no eixo y
    ax.set_ylim(bottom=0)  # Garantir que o eixo y comece a partir de 0
    
# Ajustar o layout e mostrar o gráfico
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()