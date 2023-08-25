import requests
from config import access_token
from datetime import datetime


def get_repositories():
    url = 'https://api.github.com/graphql'
    query = '''
    {
        search(query: "stars:>1", type: REPOSITORY, first: 100, after: "Y3Vyc29yOjEwMA==") {
    pageInfo {
      hasNextPage
      endCursor
    }
    edges {
      node {
        ... on Repository {
          name
          url
          releases(orderBy: {field: CREATED_AT, direction: DESC}) {
            totalCount
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
            print(f"Repositório: {repo_data['name']}")
            print(
                f"Total Releases: {repo_data['releases']['totalCount']} releases")
            print("**********")
    else:
        print("deu ruim")


if __name__ == "__main__":
    get_repositories()
