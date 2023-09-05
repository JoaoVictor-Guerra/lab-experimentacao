import requests
import csv
from config import access_token
import matplotlib.pyplot as plt
import numpy as np

def make_box_plot(arr):
    median = np.median(arr)

    plt.boxplot(arr, vert=False, whis=[25, 75])
    plt.title('Número de Releases')
    plt.xlabel('Total de Releases')

    plt.scatter([median], [1], color='red', marker='o', label='Mediana')
    plt.text(median, 1, f'Mediana: {median}', color='red',
             verticalalignment='bottom', horizontalalignment='left')

    plt.yticks([])
    plt.grid(True)
    plt.legend()
    plt.show()

def get_repositories(file_name):
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Total_releases", "URL"])
        url = 'https://api.github.com/graphql'
        repo_releases_values = []
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
                  name
                  url
                  releases(orderBy: {field: CREATED_AT, direction: DESC}) {
                      totalCount
                  }
                }
              }
            }
          }
        }'''
        pagination_query = query

        header_config = {
            'Authorization': f'Bearer {access_token}'
        }

        csv_data = []
        for i in range(0, 10):
            response = requests.post(
                url, json={'query': pagination_query}, headers=header_config)

            if response.status_code == 200:
                data = response.json()
                repositories = data['data']['search']['edges']

                for repository in repositories:
                    repo_data = repository['node']
                    csv_data += [[repo_data['name'], repo_data['releases']
                                  ['totalCount'], repo_data['url']]]

                    #Data
                    repo_releases_values.append(repo_data['releases']['totalCount'])

                has_next_page = data['data']['search']['pageInfo']['hasNextPage']
                print(has_next_page)
                if has_next_page == False:
                    break

                end_cursor = (
                    f"\"{data['data']['search']['pageInfo']['endCursor']}\"")
                pagination_query = query.replace('null', end_cursor)

            else:
                print("--------------DEU RUIM--------------")

        writer.writerows(csv_data)
        file.close
        make_box_plot(repo_releases_values)


if __name__ == "__main__":
    get_repositories("LAB01/Resultados/lab01RQ03.csv")
