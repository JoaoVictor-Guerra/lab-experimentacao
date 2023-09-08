import requests
import csv
from config import access_token
import matplotlib.pyplot as plt
import numpy as np


def make_box_plot(arr):
    median = np.median(arr)

    plt.boxplot(arr, vert=False, whis=[25, 75])

    plt.scatter([median], [1], color='red', marker='o', label='Mediana')
    plt.text(median, 1, f'Mediana: {median}', color='red',
             verticalalignment='bottom', horizontalalignment='left')

    plt.title('Percentual de Issues Fechadas')
    plt.xlabel('Número de Issues fechadas pelo total de Issues')
    plt.yticks([])
    plt.grid(True)
    plt.legend()
    plt.show()


def calculate_percentage(open_issues, closed_issues):
    total_issues = open_issues+closed_issues
    if total_issues == 0:
        return None
    percentage = (closed_issues/total_issues)
    return f'{percentage:.3f}'


def get_repositories(file_name):
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Language", "URL"])
        url = 'https://api.github.com/graphql'
        cursor = None
        repo_issues_values = []

        csv_data = []
        for c in range(10):
            query = '''
          query($cursor: String){
        search(query: "stars:>100", type: REPOSITORY, first: 100, after: $cursor) {
          edges {
            node {
              ... on Repository {
                name
                url
                openIssues: issues(states: OPEN) {
                  totalCount
                }
                closedIssues: issues(states: CLOSED) {
                  totalCount
                }
              }
            }
          }
          pageInfo{
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
                    open_issues = repo_data['openIssues']['totalCount']
                    closed_issues = repo_data['closedIssues']['totalCount']
                    csv_data += [[repo_data['name'], calculate_percentage(
                        open_issues, closed_issues), repo_data['url']]]

                    if calculate_percentage(open_issues, closed_issues) is not None:
                        repo_issues_values.append(
                            float(calculate_percentage(open_issues, closed_issues)))

                cursor = data['data']['search']['pageInfo']['endCursor']
            else:
                print("deu ruim")
        print("Acabou")
        writer.writerows(csv_data)
        file.close
        # print(repo_issues_values)
        make_box_plot(repo_issues_values)


if __name__ == "__main__":
    get_repositories("LAB01/Resultados/lab01RQ06.csv")
