import requests
import csv
from config import access_token
from time import sleep

def get_github_link(nameWithOwner):
    return f'https://github.com/{nameWithOwner}'

header_config = {'Authorization': f'Bearer {access_token}'}
url = 'https://api.github.com/graphql'

query = """
query ($cursor: String) {
    search(query: "stars:>100", type: REPOSITORY, first: 100, after: $cursor) {
        nodes {
            ... on Repository {
                id
                nameWithOwner
            }
        }
        pageInfo {
            endCursor
            hasNextPage
        }
    }
}
"""

variables = {"cursor": None}
analyzed_repositories = []

while len(analyzed_repositories) < 200: 
    response = requests.post(
        url, json={'query': query, 'variables': variables}, headers=header_config)

    if response.status_code == 200:
        data = response.json()
        repositories = data['data']['search']['nodes']

        for repo in repositories:
            nameWithOwner = repo['nameWithOwner']
            github_link = get_github_link(nameWithOwner)
            analyzed_repositories.append({'nameWithOwner': nameWithOwner, 'github_link': github_link})

        hasNextPage = data['data']['search']['pageInfo']['hasNextPage']

        if not hasNextPage:
            break

        cursor = data['data']['search']['pageInfo']['endCursor']
        variables["cursor"] = cursor

        sleep(5)

    else:
        print(f"Erro {response.status_code}")
        break


with open('analyzed_repositories.csv', 'w', newline='') as csvfile:
    fieldnames = ['nameWithOwner', 'github_link']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for repo in analyzed_repositories:
        writer.writerow({'nameWithOwner': repo['nameWithOwner'], 'github_link': repo['github_link']})

print("cabou")
