import requests
from config import access_token
from datetime import datetime

cursor = None
header_config = {'Authorization': f'Bearer {access_token}'}
url = 'https://api.github.com/graphql'

for c in range(2): 
    query = """
    query ($cursor: String) {
        search(query: "is:pr is:merged is:closed review:required", type: ISSUE, first: 100, after: $cursor) {
            edges {
                node {
                    ... on PullRequest {
                        createdAt
                        closedAt
                        mergedAt
                        repository {
                            nameWithOwner
                        }
                        reviews(first: 1) {
                            totalCount
                        }
                    }
                }
            }
            pageInfo {
                endCursor
                hasNextPage
            }
        }
    }
    """

    variables = {
        "cursor": cursor
    }

    response = requests.post(
        url, json={'query': query, 'variables': variables}, headers=header_config)

    if response.status_code == 200:
        data = response.json()

        prs = data['data']['search']['edges']
        new_prs = []

        for pr in prs:
            node = pr['node']

            review_count = node['reviews']['totalCount']

            created_at = datetime.strptime(
                node['createdAt'], '%Y-%m-%dT%H:%M:%SZ')

            closed_at = datetime.strptime(
                node['closedAt'], '%Y-%m-%dT%H:%M:%SZ') if node['closedAt'] else None

            merged_at = datetime.strptime(
                node['mergedAt'], '%Y-%m-%dT%H:%M:%SZ') if node['mergedAt'] else None

            if (merged_at and (merged_at - created_at).total_seconds() > 3600) or \
                    (closed_at and (closed_at - created_at).total_seconds() > 3600):
                new_prs.append({
                    'repository': node['repository']['nameWithOwner'],
                    'created_at': created_at,
                    'closed_at': closed_at,
                    'merged_at': merged_at,
                    'review_count': review_count
                })

        if not new_prs:
            print("Nenhum PR encontrado com mais de 1h de duração entre a abertura e o fechamento")
            break

        for pr in new_prs:
            print("Repositório:", pr['repository'])
            print("Criação:", pr['created_at'])
            print("Fechamento:", pr['closed_at'])
            print("Merge:", pr['merged_at'])
            print("Número de Revisões:", pr['review_count'])
            print("\n")

        hasNextPage = data['data']['search']['pageInfo']['hasNextPage']

        if not hasNextPage:
            break

        cursor = data['data']['search']['pageInfo']['endCursor']
    else:
        print('lascou')
