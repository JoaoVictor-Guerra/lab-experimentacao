import requests
import csv
from config import access_token
from datetime import datetime
from enum import Enum
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

def make_graph(arr):
    plt.title('Linguagens de Programação')
    counter = Counter(arr)
    
    sorted_items = sorted(counter.items(), key=lambda x: x[1], reverse=True)
    sorted_languages, sorted_counts = zip(*sorted_items)
    
    plt.bar(sorted_languages, sorted_counts)
    
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()


class TopProgrammingLanguages(Enum):
    JAVASCRIPT = 'JavaScript'
    PYTHON = 'Python'
    JAVA = 'Java'
    TYPESCRIPT = 'Typescript'
    C_SHARP = 'C#'
    CPP = 'C++'
    PHP = 'PHP'
    SHELL = 'Shell'
    C = 'C'
    RUBY = 'Ruby'


def get_last_update_age(updated_at):
    date_now = datetime.now()
    update_date = datetime.strptime(updated_at, "%Y-%m-%dT%H:%M:%SZ")
    age = date_now - update_date
    if (age.days < 0):
        return 0
    return age.days


def get_repositories(file_name):
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Language", "URL"])
        url = 'https://api.github.com/graphql'
        cursor = None
        repo_lang_values = []

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
                    languages(first: 1, orderBy: {field: SIZE, direction: DESC}) {
                      edges {
                        node {
                          name
                        }
                      }
                    }
                  }
                }
              }
              pageInfo{
                endCursor
                hasNextPage
              }
            }
          } '''
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
                    if bool(repo_lang):
                        csv_data += [[repo_data['name'],
                                      repo_lang[0]['node']['name'], repo_data['url']]]
                        # Data
                        repo_lang_values.append(repo_lang[0]['node']['name'])
                    else:
                        csv_data += [[repo_data['name'],
                                      'none', repo_data['url']]]

                        

                cursor = data['data']['search']['pageInfo']['endCursor']
            else:
                print("deu ruim")
        print("Acabou")
        writer.writerows(csv_data)
        file.close
        make_graph(repo_lang_values)


if __name__ == "__main__":
    get_repositories("LAB01/Resultados/lab01RQ05.csv")
