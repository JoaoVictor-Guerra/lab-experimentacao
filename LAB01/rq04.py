import requests
from config import access_token
from datetime import datetime


def get_last_update_age(updated_at):
    date_now = datetime.now()
    update_date = datetime.strptime(updated_at, "%Y-%m-%dT%H:%M:%SZ")
    age = date_now - update_date
    return age.days


def get_repositories():
    url = 'https://api.github.com/graphql'
    query = '''
    {
      search(query: "stars:>100", type: REPOSITORY, first: 100, after: null) {
        pageInfo {
          hasNextPage
          endCursor
        }
        edges {
          node {
            ... on Repository {
              url
              name
              updatedAt
            }
          }
        }
      }
    } '''
    pagination_query = query

    header_config = {
        'Authorization': f'Bearer {access_token}'
    }

    for i in range(0, 10):
        response = requests.post(
            url, json={'query': pagination_query}, headers=header_config)

        if response.status_code == 200:

            data = response.json()
            repositories = data['data']['search']['edges']

            for repository in repositories:
                repo_data = repository['node']
                update_age = get_last_update_age(repo_data['updatedAt'])
                print(f"Repositório: {repo_data['name']}")
                print(f"Link: {repo_data['url']}")
                print(f"Idade update: {update_age} dias")
                print("******************")

            has_next_page = data['data']['search']['pageInfo']['hasNextPage']
            if has_next_page == False:
                break
            
            end_cursor = (
                f"\"{data['data']['search']['pageInfo']['endCursor']}\"")
            pagination_query = query.replace('null', end_cursor)

        else:
            print("--------------DEU RUIM--------------")


if __name__ == "__main__":
    get_repositories()
