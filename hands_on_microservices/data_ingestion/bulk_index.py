import csv
from elasticsearch import Elasticsearch, helpers
import os

# Configuration
CSV_FILE = "language_detection_data_s.csv"
INDEX_NAME = "language_detection"

# Connexion à Elasticsearch (utilise le port interne 9200)
es = Elasticsearch([{"host": "elasticsearch", "port": 9200, "scheme": "http"}])

mapping = {
    "mappings": {
        "properties": {
            "text": {"type": "text"},
            "language": {"type": "keyword"},
            "created_at": {"type": "date"}  # Champ pour trier les documents
        }
    }
}

if not es.indices.exists(index="language_detection"):
    es.indices.create(index="language_detection", body=mapping)
    print("Index 'language_detection' créé.")


def generate_actions(csv_file_path):
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        # Utilise DictReader pour lire les colonnes en fonction de l'en-tête CSV
        reader = csv.DictReader(csvfile)
        for row in reader:
            # On nettoie les espaces superflus
            text = row.get("Text", "").strip()
            language = row.get("Language", "").strip()
            # On ignore les lignes vides (si besoin)
            if text:
                yield {
                    "_index": INDEX_NAME,
                    "_source": {
                        "text": text,
                        "language": language
                    }
                }

if __name__ == "__main__":
    if not os.path.exists(CSV_FILE):
        print(f"Le fichier {CSV_FILE} n'existe pas.")
    else:
        success, _ = helpers.bulk(es, generate_actions(CSV_FILE))
        print(f"Indexation terminée. {success} documents indexés.")
