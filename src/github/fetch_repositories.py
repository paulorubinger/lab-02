from dotenv import load_dotenv
import os
import requests
import csv
import time

load_dotenv()

BASE_URL = "https://api.github.com/search/repositories"
OUTPUT_FILE = "data/raw/top_1000_java_repositories.csv"

TOKEN = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"token {TOKEN}"
}

def fetch_top_java_repositories():
    repositories = []

    for page in range(1, 11):
        
        params = {
            "q": "language:Java",
            "sort": "stars",
            "order": "desc",
            "per_page": 100,
            "page": page
        }

        print(f"Fetching page {page}...")

        response = requests.get(BASE_URL, headers=headers, params=params)

        if response.status_code != 200:
            print("Error fetching data:", response.status_code)
            break

        data = response.json()

        for repo in data["items"]:
            repositories.append({
                "name": repo["full_name"],
                "stars": repo["stargazers_count"],
                "url": repo["clone_url"],
                "created_at": repo["created_at"]
            })

        time.sleep(1)

    save_to_csv(repositories)
    print("Finished! CSV file created.")

def save_to_csv(repositories):
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["name", "stars", "url", "created_at"])
        writer.writeheader()
        writer.writerows(repositories)