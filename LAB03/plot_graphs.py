import pandas as pd
import matplotlib.pyplot as plt
import os

if not os.path.exists('plots'):
    os.makedirs('plots')

df = pd.read_csv('pr_data.csv')

# RQ 05: Qual a relação entre o tamanho dos PRs e o número de revisões realizadas?
plt.scatter(df['changedFiles'], df['reviews_totalCount'], alpha=0.5)
plt.xlabel('Tamanho dos PRs (número de arquivos)')
plt.ylabel('Número de revisões')
plt.title('Relação entre o tamanho dos PRs e o número de revisões')
plt.savefig('plots/RQ05_tamanho_revisoes.png')
plt.show()

# RQ 06: Qual a relação entre o tempo de análise dos PRs e o número de revisões realizadas?
plt.scatter((pd.to_datetime(df['mergedAt']) - pd.to_datetime(df['createdAt'])).dt.days, df['reviews_totalCount'], alpha=0.5)
plt.xlabel('Tempo de Análise dos PRs (em dias)')
plt.ylabel('Número de revisões')
plt.title('Relação entre o tempo de análise dos PRs e o número de revisões')
plt.savefig('plots/RQ06_tempo_analise_revisoes.png')
plt.show()

# RQ 07: Qual a relação entre a descrição dos PRs e o número de revisões realizadas?
plt.scatter(df['body'].str.len(), df['reviews_totalCount'], alpha=0.5)
plt.xlabel('Tamanho da descrição dos PRs (em número de caracteres)')
plt.ylabel('Número de revisões')
plt.title('Relação entre a descrição dos PRs e o número de revisões')
plt.savefig('plots/RQ07_descricao_revisoes.png')
plt.show()

# RQ 08: Qual a relação entre as interações nos PRs e o número de revisões realizadas?
plt.scatter(df['participants_totalCount'], df['reviews_totalCount'], alpha=0.5)
plt.xlabel('Número de participantes nos PRs')
plt.ylabel('Número de revisões')
plt.title('Relação entre as interações nos PRs e o número de revisões')
plt.savefig('plots/RQ08_interacoes_revisoes.png')
plt.show()
