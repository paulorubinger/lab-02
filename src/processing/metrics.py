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

    # Resolve caminhos absolutos para evitar problemas com cwd
    abs_repo_path = os.path.abspath(repo_path)
    abs_ck_jar = os.path.abspath(ck_jar)
    abs_output_folder = os.path.abspath(output_folder)

    print(f"Analyzing repository: {repo_path}...")

    # Executa o CK com cwd=output_folder para que os CSVs sejam gerados lá
    subprocess.run([
        "java", "-jar", abs_ck_jar, abs_repo_path, "true", "0", "true"
    ], check=True, cwd=abs_output_folder)

    print("Metrics collected!")

if __name__ == "__main__":
    run_ck(REPO_PATH, CK_JAR, OUTPUT_FOLDER)