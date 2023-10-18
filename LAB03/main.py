import csv
import requests
from config import access_token
from datetime import datetime, timedelta

def get_pr_data(owner, name):
    query = """
    {
        repository(owner: "%s", name: "%s") {
            pullRequests(first: 100, orderBy: {field: CREATED_AT, direction: ASC}) {
                nodes {
                    author {
                        login
                    }
                    body
                    closed
                    closedAt
                    createdAt
                    deletions
                    id
                    lastEditedAt
                    merged
                    mergedAt
                    number
                    state
                    title
                    reviews {
                        totalCount
                    }
                    participants {
                        totalCount
                    }
                    comments {
                        totalCount
                    }
                }
            }
        }
    }
    """ % (owner, name)

    headers = {'Authorization': f'Bearer {access_token}'}
    url = 'https://api.github.com/graphql'
    data = {
        'query': query
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        data = response.json()
        pull_requests = data.get('data', {}).get('repository', {}).get('pullRequests', {}).get('nodes', [])
        return pull_requests
    else:
        print(f"Erro {response.status_code}")
        return []


csv_filename = 'analyzed_repositories.csv'
repositories = []

with open(csv_filename, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        nameWithOwner = row['nameWithOwner']
        owner, name = nameWithOwner.split('/')
        repositories.append({'nameWithOwner': nameWithOwner, 'owner': owner, 'name': name})


pr_data = []

for repo in repositories:
    owner = repo['owner']
    name = repo['name']
    pull_requests = get_pr_data(owner, name)

    for pr in pull_requests:
        created_at = pr.get('createdAt')
        closed_at = pr.get('closedAt')
        merged_at = pr.get('mergedAt')

        if created_at and (closed_at or merged_at):

            created_time = datetime.fromisoformat(created_at[:-1])
            closed_time = datetime.fromisoformat(closed_at[:-1]) if closed_at else None
            merged_time = datetime.fromisoformat(merged_at[:-1]) if merged_at else None

            time_threshold = timedelta(hours=1)

            if (closed_time and closed_time - created_time > time_threshold) or (merged_time and merged_time - created_time > time_threshold):
                # print(f"Pull Request - {pr.get('title', 'Sem título')}")
                # print(f"Repositório: {repo['nameWithOwner']}")
                # print(f"Estado: {pr.get('state', 'Desconhecido')}")
                # print(f"Criado em: {created_at}")
                # print(f"Fechado: {pr.get('closed', False)}")
                # print(f"Merged: {pr.get('merged', False)}")
                # print(f"Data de Fechamento: {closed_at if closed_at else 'Não fechado'}")
                # print(f"Data de Merge: {merged_at if merged_at else 'Não mergeado'}")
                # print(f"Número de Reviews: {pr.get('reviews', {}).get('totalCount', 0)}")
                # print(f"Número de Participantes: {pr.get('participants', {}).get('totalCount', 0)}")
                # print(f"Número de Comentários: {pr.get('comments', {}).get('totalCount', 0)}")
                # print(f"Número de Arquivos Alterados: {pr.get('deletions', 0)}")
                # print(f"Número de Linhas Deletadas: {pr.get('deletions', 0)}")
                # print(f"Descrição: {pr.get('body', 'Sem descrição')}")
                # print("\n")

                pr_data.append({
                    'nameWithOwner': repo['nameWithOwner'],
                    'title': pr.get('title', ''),
                    'state': pr.get('state', ''),
                    'createdAt': created_at,
                    'closed': pr.get('closed', False),
                    'merged': pr.get('merged', False),
                    'closedAt': closed_at,
                    'mergedAt': merged_at,
                    'reviews_totalCount': pr.get('reviews', {}).get('totalCount', 0),
                    'participants_totalCount': pr.get('participants', {}).get('totalCount', 0),
                    'comments_totalCount': pr.get('comments', {}).get('totalCount', 0),
                    'changedFiles': pr.get('deletions', 0),
                    'deletions': pr.get('deletions', 0),
                    'body': pr.get('body', '')
                })


with open('pr_data.csv', 'w', newline='') as csvfile:
    fieldnames = ['nameWithOwner', 'title', 'state', 'createdAt', 'closed', 'merged',
                  'closedAt', 'mergedAt', 'reviews_totalCount', 'participants_totalCount',
                  'comments_totalCount', 'changedFiles', 'deletions', 'body']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(pr_data)

print("deu bom")
