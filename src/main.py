from github_api.repositories import fetch_repositories
from processing.metrics import extract_metrics
from utils.save_csv import save_to_csv
from utils.load_query import load_query

def main():

    query = load_query("src/github_api/queries/top_java_repositories.graphql")

    nodes = fetch_repositories(query, 1000)

    repositories = [extract_metrics(repo) for repo in nodes]

    save_to_csv(repositories, "data/raw/repositories.csv")

if __name__ == "__main__":
    main()