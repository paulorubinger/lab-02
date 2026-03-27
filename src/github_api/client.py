import os
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_API_URL = "https://api.github.com/graphql"
TOKEN = os.getenv("GITHUB_TOKEN")

if not TOKEN:
    raise RuntimeError("Defina a variável de ambiente GITHUB_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {TOKEN}"
}

def run_query(query: str) -> dict:
    response = requests.post(
        GITHUB_API_URL,
        json={"query": query},
        headers=HEADERS,
    )

    if response.status_code != 200:
        print(response.text)
        raise RuntimeError("Erro ao consultar a API do GitHub GraphQL")

    return response.json()