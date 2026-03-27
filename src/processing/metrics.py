def extract_metrics(repo):
    return {
        "owner": repo.get("owner", {}).get("login"),
        "repository": repo.get("name"),
        "stars": repo.get("stargazerCount"),
        "created_at": repo.get("createdAt"),
        "releases": repo.get("releases", {}).get("totalCount"),
        "url": repo.get("url")
    }