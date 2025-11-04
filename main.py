from fastapi import FastAPI, Query
from typing import Optional
from pydantic import BaseModel


app = FastAPI()

@app.get("/users")
async def get_users():
    return "Hello World"


fake_items = [{"item_name": "Foo"}, {"item_name": "Baz"}, {"item_name": "Bar"}]

@app.get("/items")
async def list_items(skip: int = 0, limit: int = 10):
    return fake_items[skip: skip + limit] 


@app.get("/items/{item_id}")
async def get_item(item_id: int, question: str, q: Optional[str] = None, short: Optional[bool] = False):
    
    item = {"item_id": item_id, "question": question}
    
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "Lorem Ipsum is a dummy text commonly used in the printing and typesetting "})
    
    return item


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = 0


@app.post("/items")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price with tax": price_with_tax})
    return item_dict


@app.get("/item")
async def read_item(q: Optional[str] = Query(None, min_length=3, max_length=10, regex="ppp")):
    result = {"items": [{"name": "bar"}, {"name": "foo"}]}
    if q:
        result.update({"q": q})
    return result