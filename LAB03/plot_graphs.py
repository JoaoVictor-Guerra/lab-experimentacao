import pandas as pd
import matplotlib.pyplot as plt

# Pathing
if not os.path.exists('plots'):
    os.makedirs('plots')

boxplots_dir = os.path.join('plots', 'boxplots')
if not os.path.exists(boxplots_dir):
    os.makedirs(boxplots_dir)

def generate_boxplot(data, ylabel, title, filename):
    plt.figure(figsize=(8, 6))
    plt.boxplot(data, vert=False)
    medians = [f'{median:.2f}' for median in data]
    for i, median in enumerate(data):
        plt.text(median, i + 1, medians[i], horizontalalignment='center', verticalalignment='center', fontsize=10, color='red')
    plt.yticks([1], ['CLOSED'])

    plt.xlabel(ylabel)
    plt.title(title)
    plt.grid(True)

    plt.savefig(f'plots/boxplots/closed/{filename}', dpi=300)
    plt.close()


data = pd.read_csv("pr_data.csv")

closed_prs = data[data['state'] == 'CLOSED']

# RQ 01 - Relação entre o tamanho dos PRs (número de arquivos deletados) e o feedback final das revisões
generate_boxplot(closed_prs['deletions'], 'Tamanho (número de arquivos deletados)', 'RQ01 Tamanho x Feedback', 'tamanho_feedback_closed.png')

# RQ 02 - Relação entre o tempo de análise dos PRs e o feedback final das revisões 
closed_prs['tempo_analise'] = (pd.to_datetime(closed_prs['closedAt']) - pd.to_datetime(closed_prs['createdAt'])).dt.days
generate_boxplot(closed_prs['tempo_analise'], 'Tempo de Análise (dias)', 'RQ02 Tempo de Análise x Feedback', 'tempo_analise_feedback_closed.png')

# RQ 03 - Relação entre a descrição dos PRs (número de caracteres do corpo) e o feedback final das revisões 
closed_prs['tamanho_descricao'] = closed_prs['body'].str.len()
generate_boxplot(closed_prs['tamanho_descricao'], 'Tamanho da Descrição', 'RQ03 Descrição x Feedback', 'descricao_feedback_closed.png')

# RQ 04 - Relação entre as interações nos PRs e o feedback final das revisões
generate_boxplot(closed_prs['participants_totalCount'], 'Número de Participantes', 'RQ04 Interações x Feedback', 'interacoes_feedback_closed.png')


# Merged

merged_dir = os.path.join(boxplots_dir, 'merged')
if not os.path.exists(merged_dir):
    os.makedirs(merged_dir)


df = pd.read_csv('pr_data.csv')
merged_prs = df[df['merged']]

# RQ 01: Relação entre o tamanho dos PRs (número de arquivos) e o feedback final (merged)
sizes = [merged_prs['deletions']]
labels = ['MERGED']

plt.boxplot(sizes, vert=False, labels=labels, showfliers=False)
plt.xlabel('Tamanho dos PRs (em número de linhas deletadas)')
plt.title('Relação entre o tamanho dos PRs mergeados e Feedback Final das Revisões')
plt.figtext(0.65, 0.7, f'Mediana: {merged_prs["deletions"].median()}', fontsize=10, color='red')
plt.savefig(os.path.join(merged_dir, 'RQ01_tamanho_feedback_merged.png'))
plt.show()

# RQ 02: Relação entre o tempo de análise dos PRs e o feedback final (merged)
merged_prs['tempo_analise'] = (pd.to_datetime(merged_prs['mergedAt']) - pd.to_datetime(merged_prs['createdAt'])).dt.days

sizes = [merged_prs['tempo_analise']]
labels = ['MERGED']

plt.boxplot(sizes, vert=False, labels=labels, showfliers=False)
plt.xlabel('Tempo de Análise dos PRs (dias)')
plt.title('Relação entre o tempo de análise dos PRs merged e Feedback Final das Revisões')
plt.figtext(0.65, 0.7, f'Mediana: {merged_prs["tempo_analise"].median()}', fontsize=10, color='red')
plt.savefig(os.path.join(merged_dir, 'RQ02_tempo_analise_feedback_merged.png'))
plt.show()

# RQ 03: Relação entre o tamanho da descrição dos PRs e o feedback final (merged)
merged_prs['tamanho_descricao'] = merged_prs['body'].str.len()

sizes = [merged_prs['tamanho_descricao']]
labels = ['MERGED']

plt.boxplot(sizes, vert=False, labels=labels, showfliers=False)
plt.xlabel('Tamanho da descrição dos PRs (número de caracteres)')
plt.title('Relação entre o tamanho da descrição dos PRs merged e Feedback Final das Revisões')
plt.figtext(0.65, 0.7, f'Mediana: {merged_prs["tamanho_descricao"].median()}', fontsize=10, color='red')
plt.savefig(os.path.join(merged_dir, 'RQ03_tamanho_descricao_feedback_merged.png'))
plt.show()


# RQ 04: Relação entre as interações nos PRs e o feedback final (merged)
sizes = [merged_prs['participants_totalCount'], merged_prs['comments_totalCount']]
labels = ['Participantes', 'Comentários']

plt.boxplot(sizes, vert=False, labels=labels, showfliers=False)
plt.xlabel('Interações nos PRs')
plt.title('Relação entre as interações nos PRs merged e Feedback Final das Revisões')
plt.figtext(0.65, 0.7, f'Mediana - Participantes: {merged_prs["participants_totalCount"].median()}', fontsize=10, color='red')
plt.figtext(0.65, 0.6, f'Mediana - Comentários: {merged_prs["comments_totalCount"].median()}', fontsize=10, color='green')
plt.savefig(os.path.join(merged_dir, 'RQ04_interacoes_feedback_merged.png'))
plt.show()


# PERGUNTAS B

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
