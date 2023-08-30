import requests
import csv
from config import access_token


def get_repositories(file_name):
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Owner_login", "Accepted_PRs", "URL"])
        url = 'https://api.github.com/graphql'
        cursor = None

        csv_data = []
        for c in range(10):
            query = '''
            query ($cursor: String){
                search(query: "stars:>100", type: REPOSITORY, first: 100, after: $cursor) {
                    edges {
                        node {
                            ... on Repository {
                                name
                                url
                                owner {
                                    login
                                }
                                pullRequests(states: MERGED) {
                                    totalCount
                                }
                            }
                        }
                    }
                    pageInfo {
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
                    csv_data += [[repo_data['name'], repo_data['owner']['login'],
                                  repo_data['pullRequests']['totalCount'], repo_data['url']]]

                cursor = data['data']['search']['pageInfo']['endCursor']
            else:
                print("deu ruim")
        print("Acabou")
        writer.writerows(csv_data)
        file.close


if __name__ == "__main__":
    get_repositories("LAB01/Resultados/lab01RQ02.csv")
