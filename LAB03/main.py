import csv
import requests
from config import access_token
from datetime import datetime, timedelta
import time

def get_pr_data(owner, name):
    query = """
    query ($owner: String!, $name: String!, $cursor: String) {
        repository(owner: $owner, name: $name) {
            pullRequests(first: 30, after: $cursor, states: [CLOSED, MERGED]) {
                edges {
                    node {
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
                pageInfo {
                    endCursor
                    hasNextPage
                }
            }
        }
    }
    """

    headers = {'Authorization': f'Bearer {access_token}'}
    url = 'https://api.github.com/graphql'

    cursor = None
    pr_data = []

    while True:
        data = {
            'query': query,
            'variables': {
                'owner': owner,
                'name': name,
                'cursor': cursor
            }
        }

        response = requests.post(url, json=data, headers=headers)

        # print('+1')

        if response.status_code != 200:
            print(f"Erro {response.status_code}")
            break

        data = response.json()

        pull_requests = data.get('data', {}).get('repository', {}).get('pullRequests', {}).get('edges', [])
        nextPageInfo = data.get('data', {}).get('repository', {}).get('pullRequests', {}).get('pageInfo', {})

        if not pull_requests:
            break

        for pr_edge in pull_requests:
            pr = pr_edge['node']
            created_at = pr.get('createdAt')
            closed_at = pr.get('closedAt')
            merged_at = pr.get('mergedAt')

            if created_at and (closed_at or merged_at):
                created_time = datetime.fromisoformat(created_at[:-1])
                closed_time = datetime.fromisoformat(closed_at[:-1]) if closed_at else None
                merged_time = datetime.fromisoformat(merged_at[:-1]) if merged_at else None

                time_threshold = timedelta(hours=1)

                if (closed_time and closed_time - created_time > time_threshold) or (merged_time and merged_time - created_time > time_threshold):
                    pr_data.append({
                        'nameWithOwner': f"{owner}/{name}",
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
                        'changedFiles': pr.get('changedFiles', 0),
                        'deletions': pr.get('deletions', 0),
                        'body': pr.get('body', '')
                    })

        if not nextPageInfo.get('hasNextPage'):
            break

        cursor = nextPageInfo.get('endCursor')

        time.sleep(1)

    return pr_data


prs_analisados = 0

csv_filename = 'analyzed_repositories.csv'
repositories = []

with open(csv_filename, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        nameWithOwner = row['nameWithOwner']
        owner, name = nameWithOwner.split('/')
        repositories.append({'nameWithOwner': nameWithOwner, 'owner': owner, 'name': name})


def meet_conditions(pr):
    created_at = pr.get('createdAt')
    closed_at = pr.get('closedAt')
    merged_at = pr.get('mergedAt')

    if not created_at:
        return False

    created_time = datetime.fromisoformat(created_at[:-1])

    if (closed_at or merged_at) and created_time:
        closed_time = datetime.fromisoformat(closed_at[:-1]) if closed_at else None
        merged_time = datetime.fromisoformat(merged_at[:-1]) if merged_at else None
        time_threshold = timedelta(hours=1)

        return (closed_time and closed_time - created_time > time_threshold) or (merged_time and merged_time - created_time > time_threshold)
    return False

for repo in repositories:
    owner = repo['owner']
    name = repo['name']
    prs_analisados = get_pr_data(owner, name)

    with open('pr_data.csv', 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['nameWithOwner', 'title', 'state', 'createdAt', 'closed', 'merged',
                      'closedAt', 'mergedAt', 'reviews_totalCount', 'participants_totalCount',
                      'comments_totalCount', 'changedFiles', 'deletions', 'body']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if csvfile.tell() == 0:
            writer.writeheader()

        # Escrever no csv apenas os PRs filtrados
        filtered_prs = [pr for pr in prs_analisados if meet_conditions(pr)]
        writer.writerows(filtered_prs)

        #prs_analisados += len(prs_analisados)
        #print(f"{owner}/{name} - PRs analisados: {prs_analisados}")
