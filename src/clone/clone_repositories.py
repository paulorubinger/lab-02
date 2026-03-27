import csv
import os
import subprocess

INPUT_FILE = "data/raw/repositories.csv"
CLONE_FOLDER = "repos"
MAX_REPOS = 1

def create_clone_folder():
    os.makedirs(CLONE_FOLDER, exist_ok=True)

def clone_repository(repo_url, repo_name, index):
    destination = os.path.join(CLONE_FOLDER, repo_name)

    if os.path.exists(destination):
        print(f"{repo_name} already exists. Skipping...")
        return

    print(f"Cloning repository {index}/{MAX_REPOS}: {repo_name}")

    result = subprocess.run(["git", "clone", repo_url, destination])

    if result.returncode != 0:
        print(f"Error cloning {repo_name}")

def clone_top_repositories():
    create_clone_folder()

    with open(INPUT_FILE, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for i, repo in enumerate(reader, start=1):

            if i > MAX_REPOS:
                break

            repo_url = repo["url"]
            repo_name = f"{repo.get('owner')}_{repo.get('repository')}"
            clone_repository(repo_url, repo_name, i)

if __name__ == "__main__":
    clone_top_repositories()