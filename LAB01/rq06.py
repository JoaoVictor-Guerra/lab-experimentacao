import requests
from config import access_token
from datetime import datetime
from enum import Enum

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
  search(query: "stars:>20", type: REPOSITORY, first: 5) {
    edges {
      node {
        ... on Repository {
          name
          updatedAt
          issues(first: 100) {
            edges {
              node {
                closed
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
            issues = repo_data['issues']['edges']
            total_issues = 0
            closed_issues = 0
            for issue in issues:
                total_issues += 1
                issue_data = issue['node']
                if(issue_data['closed']):
                    closed_issues+=1
            print(f"Repositório: {repo_data['name']}")
            print(f"Total Issues: {total_issues}")
            print(f"Issues Fechadas: {closed_issues}")
            print(f"Issues Abertas: {total_issues - closed_issues}")
            print("**********")
    else:
        print("deu ruim")


if __name__ == "__main__":
    get_repositories()
