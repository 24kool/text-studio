# https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status
# uvicorn main:app --reload
# curl -X POST -H "Content-Type: application/json" 'http://localhost:8000/items?item=orange'
# curl -X GET http://localhost:8000/items 
# curl -X GET http://localhost:8000/items/0

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

items = []

app = FastAPI()

class ItemRequest(BaseModel):
    item: str

@app.get("/")
def root():
    return {"Hello": "World!"}

@app.post("/items")
def create_item(request: ItemRequest):
    items.append(request.item)
    return items

@app.get("/items")
def list_items(limit: int = 10):
    return items[:limit]

@app.get("/items/{index}")
def get_item(index: int):
    if index < 0 or index >= len(items):
        raise HTTPException(status_code=404, detail=f"Item {index} not found")
    return items[index]