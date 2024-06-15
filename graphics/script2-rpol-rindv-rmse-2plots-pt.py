import matplotlib.pyplot as plt
import numpy as np

# Dados extraídos das tabelas fornecidas
dados = {
    'MovieLens-1M': {
        'α': [0, 0.2, 0.4, 0.6, 0.8],
        r'$R_{pol}$': [0.127705059, 0.092975306, 0.065485454, 0.045046727, 0.027279156],
        r'$R_{indv}$': [0.034572808, 0.033503484, 0.030058334, 0.026021418, 0.023797359],
        r'$RMSE$': [0.875528094, 0.879731532, 0.892053897, 0.910152787, 0.935862058]
    },
    'GoodBooks-10k': {
        'α': [0, 0.2, 0.4, 0.6, 0.8],
        r'$R_{pol}$': [0.254573171, 0.177911196, 0.128459384, 0.083471240, 0.056132575],
        r'$R_{indv}$': [0.058675519, 0.056173741, 0.051789997, 0.044843601, 0.038740893],
        r'$RMSE$': [0.855771561, 0.860838742, 0.873177885, 0.895149461, 0.920223485]
    }
}

fig, axs = plt.subplots(1, 2, figsize=(15, 8))  # Ajuste do tamanho da figura
fig.suptitle('Comparação de $R_{pol}$, $R_{indv}$ e $RMSE$ por Dataset', fontsize=16)

# Iteração pelos dados para criar os gráficos
for i, (title, data) in enumerate(dados.items()):
    ax = axs[i]
    ax2 = ax.twinx()

    # Plotar Rpol e Rindv no eixo y primário
    ax.plot(data['α'], data[r'$R_{pol}$'], marker='o', linestyle='-', color='tab:blue', label=r'$R_{pol}$')
    ax.plot(data['α'], data[r'$R_{indv}$'], marker='o', linestyle='-', color='tab:green', label=r'$R_{indv}$')

    # Plotar RMSE no eixo y secundário
    ax2.plot(data['α'], data[r'$RMSE$'], marker='o', linestyle='-', color='tab:red', label=r'$RMSE$')

    # Adicionando o título do subplot
    ax.set_title(title, fontsize=14)

    # Define os ticks do eixo X para serem apenas os valores inteiros especificados
    ax.set_xticks(data['α'])
    ax.set_xlabel('Fator de Ajuste (α)')
    
    # Adicionando labels e layout dos eixos y primário
    ax.grid(True, color='lightgray')

    # Ajustando as escalas do eixo Y primário com uma margem
    y_min = min(min(data[r'$R_{pol}$']), min(data[r'$R_{indv}$']))
    y_max = max(max(data[r'$R_{pol}$']), max(data[r'$R_{indv}$']))
    y_range = y_max - y_min
    y_margin = y_range * 0.05  # Margem de 5%
    ax.set_ylim([y_min - y_margin, y_max + y_margin])  # Adicionando margem aos limites do eixo Y primário
    ax.set_yticks(np.linspace(y_min - y_margin, y_max + y_margin, num=5))  # Ajusta os ticks do eixo Y
    ax.set_facecolor('white')  # Fundo branco

    # Ajustando as escalas do eixo Y secundário com uma margem
    y_min2 = min(data[r'$RMSE$'])
    y_max2 = max(data[r'$RMSE$'])
    y_range2 = y_max2 - y_min2
    y_margin2 = y_range2 * 0.05  # Margem de 5%
    ax2.set_ylim([y_min2 - y_margin2, y_max2 + y_margin2])  # Adicionando margem aos limites do eixo Y secundário
    ax2.set_yticks(np.linspace(y_min2 - y_margin2, y_max2 + y_margin2, num=5))  # Ajusta os ticks do eixo Y secundário

    # Custom labels for the primary Y axis
    ax.set_ylabel('')  # Clear default ylabel
    y_label_x_pos = -0.20  # Initial X position for custom Y axis labels
    y_label_y_pos = 0.4
    
    # Draw colored labels on the primary Y axis
    ax.text(y_label_x_pos, y_label_y_pos, r'$R_{pol}$', color='tab:blue', transform=ax.transAxes, ha='center', va='center', rotation='vertical', fontsize=12)
    ax.text(y_label_x_pos, y_label_y_pos + 0.1, '   ', transform=ax.transAxes, ha='center', va='center', rotation='vertical', fontsize=12)
    ax.text(y_label_x_pos, y_label_y_pos + 0.2, r'$R_{indv}$', color='tab:green', transform=ax.transAxes, ha='center', va='center', rotation='vertical', fontsize=12)

    # Adicionar legenda para o eixo y secundário
    ax2.set_ylabel(r'$RMSE$', color='tab:red')

    # Adicionar a legenda
    lines_1, labels_1 = ax.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax2.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper center')

# Ajustando o espaçamento entre os subplots
fig.subplots_adjust(bottom=0.1, top=0.9, left=0.05, right=0.95, wspace=0.3)

# Ajustes finais para melhorar layout e visualização
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
