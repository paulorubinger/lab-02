from github_api.client import run_query

def fetch_repositories(query, total):

    cursor = None
    all_repos = []

    while len(all_repos) < total:

        print(f"Fetching repositories... {len(all_repos)}/{total}")

        response = run_query(query, {"cursor": cursor})

        search = response["data"]["search"]

        repos = search["nodes"]
        all_repos.extend(repos)

        page_info = search["pageInfo"]

        if not page_info["hasNextPage"]:
            break

        cursor = page_info["endCursor"]
    
    result = all_repos[:total]
    print(f"Fetching repositories... {len(result)}/{total}")
    return result