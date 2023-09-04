import requests
import csv
from config import access_token
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

def make_box_plot(arr):
    plt.boxplot(arr, vert=False, whis=[25, 75])
    plt.title('Atualizados com Frequência')
    plt.xlabel('Valores')
    plt.yticks([]) 
    plt.grid(True)
    plt.show()

def get_last_update_age(updated_at):
    date_now = datetime.now()
    update_date = datetime.strptime(updated_at, "%Y-%m-%dT%H:%M:%SZ")
    age = date_now - update_date
    return age.days


def get_repositories(file_name):
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Update_age", "URL"])
        url = 'https://api.github.com/graphql'
        repo_updated_values = []
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

        csv_data = []
        for i in range(0, 10):
            response = requests.post(
                url, json={'query': pagination_query}, headers=header_config)

            if response.status_code == 200:

                data = response.json()
                repositories = data['data']['search']['edges']

                for repository in repositories:
                    repo_data = repository['node']
                    csv_data += [[repo_data['name'],
                                  get_last_update_age(repo_data['updatedAt']), repo_data['url']]]

                    #Data
                    repo_updated_values.append(get_last_update_age(repo_data['updatedAt']))

                has_next_page = data['data']['search']['pageInfo']['hasNextPage']
                if has_next_page == False:
                    break

                end_cursor = (
                    f"\"{data['data']['search']['pageInfo']['endCursor']}\"")
                pagination_query = query.replace('null', end_cursor)

            else:
                print("--------------DEU RUIM--------------")

        writer.writerows(csv_data)
        file.close
        make_box_plot(repo_updated_values)


if __name__ == "__main__":
    get_repositories("LAB01/Resultados/lab01RQ04.csv")
    print("Acabou")
