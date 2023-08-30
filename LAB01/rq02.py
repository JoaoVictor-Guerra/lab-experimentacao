import requests
from config import access_token
from datetime import datetime

def get_repositories():
    url = 'https://api.github.com/graphql'
    cursor = None

    for c in range(10):
        query = '''
        query ($cursor: String){
            search(query: "stars:>1", type: REPOSITORY, first: 100, after: $cursor) {
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
                pageInfo {
                    endCursor
                    hasNextPage
                }
            }
        }'''
        
        header_config = {
            'Authorization': f'Bearer {access_token}'
        }

        cursor_value = {
            "cursor": cursor
        }

        response = requests.post(
            url, json={'query': query, 'variables': cursor_value}, headers=header_config)

        if response.status_code == 200:
            data = response.json()
            repositories = data['data']['search']['edges']

            for repository in repositories:
                repo_data = repository['node']
                print(f"Repositório: {repo_data['name']}")
                print(f"Proprietário: {repo_data['owner']['login']}")
                print(
                    f"PR's aceitas: {repo_data['pullRequests']['totalCount']}")
                print("**********")
            
            cursor = data['data']['search']['pageInfo']['endCursor']
        else:
            print("deu ruim")

if __name__ == "__main__":
    get_repositories()
