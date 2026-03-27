import os
import subprocess
import shutil

def extract_metrics(repo):
    return {
        "owner": repo.get("owner", {}).get("login"),
        "repository": repo.get("name"),
        "stars": repo.get("stargazerCount"),
        "created_at": repo.get("createdAt"),
        "releases": repo.get("releases", {}).get("totalCount"),
        "url": repo.get("url")
    }

CK_JAR = "ck.jar"
REPO_PATH = "repos/Snailclimb_JavaGuide"
OUTPUT_FOLDER = "data/raw/ck_metrics/Snailclimb_JavaGuide"

def run_ck(repo_path: str, ck_jar: str, output_folder: str):
    os.makedirs(output_folder, exist_ok=True)

    print(f"Analyzing repository: {repo_path}...")
    subprocess.run([
        "java", "-jar", ck_jar, repo_path, "true", "0", "true"
    ], check=True)

    expected_files = ["class.csv", "method.csv", "variable.csv", "field.csv"]

    for file_name in expected_files:
        source_file = os.path.join(repo_path, file_name)
        if os.path.exists(source_file):
            dest_file = os.path.join(output_folder, file_name)
            shutil.move(source_file, dest_file)
            print(f"Moved {file_name} to {output_folder}")
        else:
            print(f"{file_name} not found, skipping...")

    print("Metrics collected!")

if __name__ == "__main__":
    run_ck(REPO_PATH, CK_JAR, OUTPUT_FOLDER)