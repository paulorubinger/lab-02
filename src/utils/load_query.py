def load_query(query_path):
    with open(query_path, "r", encoding="utf-8") as file:
        return file.read()
