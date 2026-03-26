import csv
import os
import subprocess

INPUT_FILE = "data/raw/top_1000_java_repositories.csv"
CLONE_FOLDER = "repos"
MAX_REPOS = 1

def create_clone_folder():
    if not os.path.exists(CLONE_FOLDER):
        os.makedirs(CLONE_FOLDER)

def clone_repository(repo_url, repo_name):
    destination = os.path.join(CLONE_FOLDER, repo_name)

    if os.path.exists(destination):
        print(f"{repo_name} already exists. Skipping...")
        return

    print(f"Cloning {repo_name}...")
    subprocess.run(["git", "clone", repo_url, destination])

def clone_top_repositories():
    create_clone_folder()

    with open(INPUT_FILE, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        count = 0

        for repo in reader:
            if count >= MAX_REPOS:
                break

            repo_url = repo["url"]
            repo_name = repo["name"].replace("/", "_")

            clone_repository(repo_url, repo_name)

            count += 1

if __name__ == "__main__":
    clone_top_repositories()