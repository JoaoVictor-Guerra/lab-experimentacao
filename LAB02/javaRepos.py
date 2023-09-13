import requests
import json
import pickle
import csv
import os
from config import access_token
from datetime import datetime


url = "https://api.github.com/graphql"
cursor = None
repo_links = []
repo_data = []

def export_repo_data(arr):
    csv_arc = "github_data.csv"

    columns = ["nome", "idade", "estrelas", "releases"]

    with open(csv_arc, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        
        for repo in arr:
            writer.writerow(repo)

    repo_data.clear()

def get_repository_age(created_at):
    date_now = datetime.now()
    creation_date = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
    age = date_now - creation_date
    return age.days

for c in range(10):
    query = """
    query ($cursor: String){
        search(query: "language:Java", type: REPOSITORY, first: 100, after: $cursor) {
            edges {
                node {
                    ... on Repository {
                        nameWithOwner
                        url
                        createdAt
                        releases(orderBy: {field: CREATED_AT, direction: DESC}) {
                            totalCount
                        }
                        stargazers{
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
    }
    """

    header_config = {
        "Authorization": f"Bearer {access_token}"
    }

    cursor_value = {
        "cursor": cursor
    }

    response = requests.post(url, json={"query": query, 'variables': cursor_value}, headers=header_config)

    if response.status_code == 200:
        data = response.json()
        repositories = data["data"]["search"]["edges"]

        for repository in repositories:
            repo_name = repository["node"]["nameWithOwner"]
            repo_url = repository["node"]["url"]
            repo_date = get_repository_age(repository["node"]["createdAt"])
            repo_releases = repository["node"]["releases"]["totalCount"]
            repo_stars = repository["node"]["stargazers"]["totalCount"]

            repo_links.append(repo_url)

            # Criar um dicionário para o repositório
            repo_dict = {
                "nome": repo_name,
                "idade": repo_date,
                "estrelas": repo_stars,
                "releases": repo_releases
            }

            repo_data.append(repo_dict)

        cursor = data['data']['search']['pageInfo']['endCursor']

    else:
        print("deu ruim")

with open('LAB02/dump.py', 'wb') as arc:
    pickle.dump(repo_links, arc)

# Exportar os dados para o arquivo CSV
export_repo_data(repo_data)

#command = "python main.py"
#os.system(command)