import requests
import csv
from config import access_token
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

def make_box_plot(arr):
    median = np.median(arr)

    plt.boxplot(arr, vert=False, whis=[25, 75])
    plt.title('Idade dos Repositórios')
    plt.xlabel('Idade (em dias)')

    plt.scatter([median], [1], color='red', marker='o', label='Mediana')
    plt.text(median, 1, f'Mediana: {median}', color='red',
             verticalalignment='bottom', horizontalalignment='left')

    plt.yticks([])
    plt.grid(True)
    plt.legend()
    plt.show()

def get_repository_age(created_at):
    date_now = datetime.now()
    creation_date = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
    age = date_now - creation_date
    return age.days


def get_repositories(file_name):
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Owner_login", "Age", "URL"])
        url = 'https://api.github.com/graphql'
        cursor = None
        repo_age_values = []

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
                    csv_data += [[repo_data['name'], repo_data['owner']['login'],
                                  get_repository_age(repo_data['createdAt']), repo_data['url']]]

                    # Grafico
                    repo_age_values.append(get_repository_age(repo_data['createdAt']))

                cursor = data['data']['search']['pageInfo']['endCursor']

            else:
                print("deu ruim")
        print("Acabou")
        writer.writerows(csv_data)

        make_box_plot(repo_age_values)
        

if __name__ == "__main__":
    get_repositories("LAB01/Resultados/lab01RQ01.csv")
