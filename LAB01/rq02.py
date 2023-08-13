import requests
from config import access_token
from datetime import datetime

def get_repositories():
    url = 'https://api.github.com/graphql'
    query = '''
    {
        search(query: "stars:>1", type: REPOSITORY, first: 100) {
            edges {
                node {
                    ... on Repository {
                        name
                        owner {
                            login
                        }
                        pullRequests(states: MERGED) {
                            totalCount
                        }
                    }
                }
            }
        }
    } '''
    headerConfig = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.post(url, json={'query': query}, headers=headerConfig)

    if response.status_code == 200:

        data = response.json()
        repositories = data['data']['search']['edges']

        for repository in repositories:
            repo_data = repository['node']
            print(f"Repositório: {repo_data['name']}")
            print(f"Proprietário: {repo_data['owner']['login']}")
            print(f"PR's aceitas: {repo_data['pullRequests']['totalCount']}")
            print("*******")
    else:
        print("deu ruim")


if __name__ == "__main__":
    get_repositories()
