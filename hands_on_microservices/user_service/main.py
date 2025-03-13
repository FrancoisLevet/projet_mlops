from fastapi import FastAPI
from elasticsearch import Elasticsearch
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

# Connexion à Elasticsearch via le réseau interne (port 9200)
es = Elasticsearch([{"host": "elasticsearch", "port": 9200, "scheme": "http"}])

class UserData(BaseModel):
    text: str
    language: str

@app.post("/insert")
async def insert_data(data: UserData):
    # Convertir en dict et ajouter la date d'insertion
    doc = data.dict()
    doc["created_at"] = datetime.utcnow().isoformat()  # Format ISO pour la date UTC
    res = es.index(index="language_detection", body=doc)
    return {"status": "success", "data_id": res["_id"]}
