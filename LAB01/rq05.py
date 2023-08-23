import requests
from config import access_token
from datetime import datetime
from enum import Enum

class TopProgrammingLanguages(Enum):
    JAVASCRIPT = 'JavaScript'
    PYTHON = 'Python'
    JAVA = 'Java'
    TYPESCRIPT = 'Typescript'
    C_SHARP = 'C#'
    CPP = 'C++'
    PHP = 'PHP'
    SHELL = 'Shell'
    C = 'C'
    RUBY = 'Ruby'


def get_last_update_age(updated_at):
    date_now = datetime.now()
    update_date = datetime.strptime(updated_at, "%Y-%m-%dT%H:%M:%SZ")
    age = date_now - update_date
    if (age.days < 0):
        return 0
    return age.days

def get_repositories():
    url = 'https://api.github.com/graphql'
    query = '''
    {
      search(query: "stars:>20", type: REPOSITORY, first: 100) {
        edges {
          node {
            ... on Repository {
              name
              updatedAt
              languages(first: 3, orderBy: {field: SIZE, direction: DESC}) {
                edges {
                  node {
                    id
                    name
                  }
                }
              }
            }
          }
        }
      }
    } '''
    header_config = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.post(url, json={'query': query}, headers=header_config)

    if response.status_code == 200:

        data = response.json()
        repositories = data['data']['search']['edges']

        for repository in repositories:
            repo_data = repository['node']
            update_age = get_last_update_age(repo_data['updatedAt'])
            repo_langs = repo_data['languages']['edges']
            languages = []
            for language in repo_langs:
                lang_data = language['node']
                languages.append(lang_data['name'])
            print(f"Repositório: {repo_data['name']}")
            print(f"Idade update: {update_age} dias")
            print(f"Linguagens: {languages}")
            print("**********")
    else:
        print("deu ruim")


if __name__ == "__main__":
    get_repositories()
