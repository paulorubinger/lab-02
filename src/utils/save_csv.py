import os
import csv

def save_to_csv(repositories, OUTPUT_FILE):
    os.makedirs("data/raw", exist_ok=True)

    print(f"Creating CSV with {len(repositories)} repositories...")

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=[
            "owner",
            "repository",
            "stars",
            "releases",
            "created_at",
            "url"
        ])

        writer.writeheader()
        writer.writerows(repositories)

    print("CSV created successfully!")