from github_api.repositories import fetch_repositories
from processing.metrics import extract_metrics, run_ck_all_repos
from processing.analysis import CKAnalysis
from clone.clone_repositories import clone_repositories
from utils.save_csv import save_to_csv
from utils.load_query import load_query

def main():
    # Load the GraphQL query to fetch top Java repositories from GitHub
    query = load_query("src/github_api/queries/top_java_repositories.graphql")

    # Search for repositories using the GitHub API
    nodes = fetch_repositories(query, total=1000)

    # Extract relevant metrics from each repository
    repositories = [extract_metrics(repo) for repo in nodes]

    csv_file = "data/raw/repositories.csv"

    # Save the repository data to a CSV file
    save_to_csv(repositories, csv_file)

    # Clone the repositories using Git and save them locally
    clone_repositories(csv_file, max_repos=100)

    # Analyze the cloned repositories using CK and save the metrics
    run_ck_all_repos()

    # Perform analysis on the collected CK metrics
    print("\nStarting CK metrics analysis...")
    analysis = CKAnalysis()
    analysis.run_full_analysis()

if __name__ == "__main__":
    main()