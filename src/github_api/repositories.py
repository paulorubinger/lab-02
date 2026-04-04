from github_api.client import run_query


def transform_repository(repo_data):
    """Transform GitHub GraphQL repository data to CSV format."""
    return {
        "owner": repo_data["owner"]["login"],
        "repository": repo_data["name"],
        "stars": repo_data.get("stargazerCount", 0),
        "releases": repo_data.get("releases", {}).get("totalCount", 0),
        "created_at": repo_data.get("createdAt", ""),
        "url": repo_data.get("url", "")
    }


def fetch_repositories(query, total):

    cursor = None
    all_repos = []

    while len(all_repos) < total:

        print(f"Fetching repositories... {len(all_repos)}/{total}")

        response = run_query(query, {"cursor": cursor})

        search = response["data"]["search"]

        repos = search["nodes"]
        
        # Transform each repository to CSV format
        transformed_repos = [transform_repository(repo) for repo in repos]
        all_repos.extend(transformed_repos)

        page_info = search["pageInfo"]

        if not page_info["hasNextPage"]:
            break

        cursor = page_info["endCursor"]
    
    result = all_repos[:total]
    print(f"Fetching repositories... {len(result)}/{total}")
    return result