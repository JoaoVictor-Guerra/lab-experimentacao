import requests
from config import access_token
from datetime import datetime

def get_repository_age(created_at):
    date_now = datetime.now()
    creation_date = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
    age = date_now - creation_date
    return age.days

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
                        stargazerCount
                        createdAt
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
            repo_age = get_repository_age(repo_data['createdAt'])
            print(f"Repositório: {repo_data['name']}")
            print(f"Proprietário: {repo_data['owner']['login']}")
            print(f"Idade: {repo_age} dias")
            print(f"Estrelas: {repo_data['stargazerCount']}")
            print("*******")
    else:
        print("deu ruim")

if __name__ == "__main__":
    get_repositories()
