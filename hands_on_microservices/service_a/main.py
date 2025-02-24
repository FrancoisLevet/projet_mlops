from fastapi import FastAPI
from elasticsearch import Elasticsearch
import httpx

app = FastAPI()
es = Elasticsearch([{'host': 'elasticsearch', 'port': 9200, 'scheme': 'http'}])


@app.get("/call-service-b")
async def call_service_b():
    # Define the path to the Unix Domain Socket
    uds_path = "/tmp/service_b.sock"
    # Use a custom transport to make requests via the UDS
    transport = httpx.AsyncHTTPTransport(uds=uds_path)
    # Standard URL format without http+unix://
    url = "http://service_b/data"
    async with httpx.AsyncClient(transport=transport) as client:
        response = await client.get(url)
    return response.json()

@app.post("/index-data")
async def index_data(data: dict):
    res = es.index(index="my_index", body=data)
    return {"result": res}

@app.get("/search")
async def search(query: str):
    res = es.search(index="my_index", body={"query": {"match": {"content": query}}})
    return {"results": res['hits']['hits']}