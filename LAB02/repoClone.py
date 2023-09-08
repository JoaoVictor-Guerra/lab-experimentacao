import os
import sys
import git


def clone_repo(url):

    folder_path = os.path.join("repos", os.path.basename(url.rstrip(".git")))

    try:
        repo = git.Repo.clone_from(url, folder_path)

    except git.GitCommandError as err:
        print(err)


if __name__ == "__main__":

    url = sys.argv[1]

    if not os.path.exists("repos"):
        os.makedirs("repos")

    clone_repo(url)
