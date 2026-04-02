from github_api.repositories import fetch_repositories
from processing.metrics import extract_metrics
from clone.clone_repositories import clone_repositories
from utils.save_csv import save_to_csv
from utils.load_query import load_query

def main():
    query = load_query("src/github_api/queries/top_java_repositories.graphql")

    nodes = fetch_repositories(query, 1000)

    repositories = [extract_metrics(repo) for repo in nodes]

    csv_file = "data/raw/repositories.csv"
    save_to_csv(repositories, csv_file)

    clone_repositories(csv_file, max_repos=5)

if __name__ == "__main__":
    main()