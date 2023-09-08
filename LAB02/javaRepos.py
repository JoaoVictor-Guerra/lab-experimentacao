import requests
import json
from config import access_token

url = "https://api.github.com/graphql"
cursor = None


for c in range(10):
    query = """
    query ($cursor: String){
        search(query: "language:Java", type: REPOSITORY, first: 100, after: $cursor) {
            edges {
                node {
                    ... on Repository {
                    nameWithOwner
                    url
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
            print("Nome do Repositório: " + repo_name)
            print("Link para o Repositório: " + repo_url)
            print("*****")

        cursor = data['data']['search']['pageInfo']['endCursor']

    else:
        print("deu ruim")

