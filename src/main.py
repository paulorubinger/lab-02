from github_api.repositories import fetch_repositories
from processing.metrics import extract_metrics, run_ck_all_repos
from clone.clone_repositories import clone_repositories
from utils.save_csv import save_to_csv
from utils.load_query import load_query

def main():
    # Carrega a consulta GraphQL para buscar os repositórios
    query = load_query("src/github_api/queries/top_java_repositories.graphql")

    # Busca os repositórios usando a API do GitHub
    nodes = fetch_repositories(query, total=1000)

    # Extrai as métricas relevantes de cada repositório
    repositories = [extract_metrics(repo) for repo in nodes]

    csv_file = "data/raw/repositories.csv"

    # Salva os dados dos repositórios em um arquivo CSV
    save_to_csv(repositories, csv_file)

    # Clona os repositórios usando Git e salva localmente
    clone_repositories(csv_file, max_repos=5)

    # Analisa os repositórios clonados usando o CK e salva as métricas
    run_ck_all_repos()

if __name__ == "__main__":
    main()