from github.fetch_repositories import fetch_top_java_repositories
from clone.clone_repositories import clone_top_repositories

def main():
    fetch_top_java_repositories()
    clone_top_repositories()

if __name__ == "__main__":
    main()