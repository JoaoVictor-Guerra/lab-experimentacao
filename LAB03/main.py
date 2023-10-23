import csv
import requests
from config import access_token
from datetime import datetime, timedelta
import time
from requests.exceptions import ChunkedEncodingError, HTTPError
import urllib3.exceptions

def get_pr_data(owner, name):
    query = """
    query ($owner: String!, $name: String!, $cursor: String) {
        repository(owner: $owner, name: $name) {
            pullRequests(first: 100, after: $cursor) {
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

        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()  
        except (ChunkedEncodingError, HTTPError, urllib3.exceptions.HTTPError) as e:
            print(f"Erro na solicitação: {e}")
            time.sleep(5)  
            continue

        data = response.json()

        pull_requests = data.get('data', {}).get('repository', {}).get('pullRequests', {}).get('edges', [])
        hasNextPage = data.get('data', {}).get('repository', {}).get('pullRequests', {}).get('pageInfo', {}).get('hasNextPage', False)

        if not pull_requests:
            break

        for pr_edge in pull_requests:
            pr = pr_edge['node']
            created_at = pr.get('createdAt')
            closed_at = pr.get('closedAt')
            merged_at = pr.get('mergedAt')

            if created_at and (closed_at or merged_at):
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

        if not hasNextPage:
            break

        cursor = data.get('data', {}).get('repository', {}).get('pullRequests', {}).get('pageInfo', {}).get('endCursor', None)
        time.sleep(2)  

    return pr_data

def main():
    csv_filename = 'analyzed_repositories.csv'
    repositories = []

    with open(csv_filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            nameWithOwner = row['nameWithOwner']
            owner, name = nameWithOwner.split('/')
            repositories.append({'nameWithOwner': nameWithOwner, 'owner': owner, 'name': name})

    for repo in repositories[:70]:  # Coleta dos 70 primeiros repositórios
        owner = repo['owner']
        name = repo['name']
        pull_requests = get_pr_data(owner, name)

        with open('pr_data.csv', 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['nameWithOwner', 'title', 'state', 'createdAt', 'closed', 'merged',
                        'closedAt', 'mergedAt', 'reviews_totalCount', 'participants_totalCount',
                        'comments_totalCount', 'changedFiles', 'deletions', 'body']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerows(pull_requests)

if __name__ == "__main__":
    main()
