import os
import subprocess

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
REPOS_FOLDER = "repos"
CK_METRICS_FOLDER = "data/raw/ck_metrics"
EXPECTED_CK_FILES = ["class.csv", "method.csv"]

def run_ck(repo_path: str, ck_jar: str, output_folder: str):
    os.makedirs(output_folder, exist_ok=True)

    abs_repo_path = os.path.abspath(repo_path)
    abs_ck_jar = os.path.abspath(ck_jar)
    abs_output_folder = os.path.abspath(output_folder)

    print(f"  Analyzing: {repo_path}...")

    result = subprocess.run([
        "java", "-jar", abs_ck_jar, abs_repo_path, "false", "0", "false"
    ], cwd=abs_output_folder, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"  ERROR analyzing {repo_path}:\n{result.stderr}")
        return False

    print(f"  Done! Metrics saved to {output_folder}")
    return True

def get_repositories(repos_folder: str) -> list:
    if not os.path.exists(repos_folder):
        print(f"Repos folder '{repos_folder}' not found.")
        return []
    
    return [
        name for name in os.listdir(repos_folder)
        if os.path.isdir(os.path.join(repos_folder, name))
    ]

def is_already_analyzed(output_folder: str, expected_files: list) -> bool:
    return all(
        os.path.exists(os.path.join(output_folder, f))
        for f in expected_files
    )

def analyze_repository(
    repo_name: str,
    repo_path: str,
    ck_jar: str,
    ck_metrics_folder: str,
    expected_files: list
) -> bool:
    output_folder = os.path.join(ck_metrics_folder, repo_name)
    
    # Pula se já foi analisado (permite retomar de onde parou)
    if is_already_analyzed(output_folder, expected_files):
        print(f"  Already analyzed. Skipping...")
        return True
    
    return run_ck(repo_path, ck_jar, output_folder)

def run_ck_all_repos(
    repos_folder: str = REPOS_FOLDER,
    ck_jar: str = CK_JAR,
    ck_metrics_folder: str = CK_METRICS_FOLDER
):
    repo_names = get_repositories(repos_folder)
    
    if not repo_names:
        return
    
    total = len(repo_names)
    print(f"Found {total} repositories to analyze.\n")

    success, failed = 0, []

    for i, repo_name in enumerate(repo_names, start=1):
        repo_path = os.path.join(repos_folder, repo_name)
        print(f"[{i}/{total}] {repo_name}")

        ok = analyze_repository(repo_name, repo_path, ck_jar, ck_metrics_folder, EXPECTED_CK_FILES)
        if ok:
            success += 1
        else:
            failed.append(repo_name)

    print_summary(success, total, failed)

def print_summary(success: int, total: int, failed: list):
    print(f"\n=== Done: {success}/{total} succeeded, {len(failed)} failed ===")
    if failed:
        print("Failed repositories:")
        for name in failed:
            print(f"  - {name}")

if __name__ == "__main__":
    run_ck_all_repos()