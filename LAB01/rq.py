import requests
import csv
from config import access_token
from datetime import datetime


def get_repository_age(created_at):
    date_now = datetime.now()
    creation_date = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
    age = date_now - creation_date
    return age.days


def calculate_percentage(open_issues, closed_issues):
    total_issues = open_issues+closed_issues
    if total_issues == 0:
        return None
    percentage = (closed_issues/total_issues)
    return f'{percentage:.3f}'


def get_last_update_age(updated_at):
    date_now = datetime.now()
    update_date = datetime.strptime(updated_at, "%Y-%m-%dT%H:%M:%SZ")
    age = date_now - update_date
    return age.days


def get_repositories(file_name):
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Owner_login", "Age", "Accepted_PRs", "Total_Releases",
                        "Update_age", "Language", "Percentage_issues_closed", "URL"])
        url = 'https://api.github.com/graphql'
        cursor = None

        csv_data = []
        for c in range(10):
            query = '''
            query ($cursor: String) {
                search(query: "stars:>100", type: REPOSITORY, first: 100, after: $cursor) {
                    edges {
                        node {
                            ... on Repository {
                                name
                                url
                                owner {
                                    login
                                }
                                createdAt
                                pullRequests(states: MERGED) {
                                    totalCount
                                }
                                releases(orderBy: {field: CREATED_AT, direction: DESC}) {
                      totalCount
                  }
                  updatedAt
                  languages(first: 1, orderBy: {field: SIZE, direction: DESC}) {
                      edges {
                        node {
                          name
                        }
                      }
                    }
                            }
                            openIssues: issues(states: OPEN) {
                  totalCount
                }
                closedIssues: issues(states: CLOSED) {
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
            '''
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
                    repo_lang = repo_data['languages']['edges']
                    lang = ''
                    if bool(repo_lang):
                        lang = repo_lang[0]['node']['name'], repo_data['url']
                    else:
                        lang = 'None'
                    open_issues = repo_data['openIssues']['totalCount']
                    closed_issues = repo_data['closedIssues']['totalCount']

                    csv_data += [[repo_data['name'],
                                  repo_data['owner']['login'],
                                  get_repository_age(repo_data['createdAt']),
                                  repo_data['pullRequests']['totalCount'],
                                  repo_data['releases']['totalCount'],
                                  get_last_update_age(repo_data['updatedAt']),
                                  calculate_percentage(
                                      open_issues, closed_issues),
                                  lang,
                                  repo_data['url']]]

                cursor = data['data']['search']['pageInfo']['endCursor']

            else:
                print("deu ruim")
        print("Acabou")
        writer.writerows(csv_data)
        file.close


if __name__ == "__main__":
    get_repositories("LAB01/Resultados/lab01RQ.csv")
