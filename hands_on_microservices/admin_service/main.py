from fastapi import FastAPI
from elasticsearch import Elasticsearch
from pydantic import BaseModel

app = FastAPI()

es = Elasticsearch([{"host": "elasticsearch", "port": 9200, "scheme": "http"}])

class AdminData(BaseModel):
    id: str
    text: str
    language: str

@app.get("/get-all")
async def get_all():
    res = es.search(
        index="language_detection",
        body={
            "query": {"match_all": {}},
            "sort": [{"created_at": {"order": "desc"}}],  # Tri par date décroissante
            "size": 100  # Ajuste le nombre de résultats selon tes besoins
        }
    )
    return {"results": res['hits']['hits']}

@app.put("/update")
async def update_data(data: AdminData):
    res = es.update(index="language_detection", id=data.id, body={"doc": {"text": data.text, "language": data.language}})
    return {"status": "updated", "data_id": res["_id"]}
