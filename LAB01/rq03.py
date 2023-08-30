import requests
import csv
from config import access_token


def get_repositories(file_name):
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Total_releases", "URL"])
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


if __name__ == "__main__":
    get_repositories("LAB01/Resultados/lab01RQ03.csv")
