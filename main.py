from fastapi import FastAPI, Query, Path, Body
from typing import Optional
from pydantic import BaseModel


app = FastAPI()


@app.get("/users")
async def get_users():
    return "Hello World"


fake_items = [{"item_name": "Foo"}, {"item_name": "Baz"}, {"item_name": "Bar"}]


@app.get("/items")
async def list_items(skip: int = 0, limit: int = 10):
    return fake_items[skip : skip + limit]


@app.get("/items/{item_id}")
async def get_item(
    item_id: int, question: str, q: Optional[str] = None, short: Optional[bool] = False
):

    item = {"item_id": item_id, "question": question}

    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {
                "description": "Lorem Ipsum is a dummy text commonly used in the printing and typesetting "
            }
        )

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


@app.get("/item")  # Add  description and title
async def read_item(
    q: Optional[str] = Query(
        None, min_length=3, max_length=15, title="simple query", description="for test"
    )
):
    result = {"items": [{"name": "bar"}, {"name": "foo"}]}
    if q:
        result.update({"q": q})
    return result


@app.get("/items_hidden")  # Add hidden query
async def hidden_query_route(hidden_query: Optional[str] = None):
    if hidden_query:
        return {"hidden query": hidden_query}
    return {"not found"}


# about [gt, ge, le, and lt] in int of (item_id)
@app.get("/items_validation/{item_id}")
async def read_item_validation(
    *,
    item_id: Optional[int] = Path(..., title="this is good path", gt=1, lt=20),
    q: Optional[str] = "Test",
    size: Optional[float] = Query(..., gt=0, lt=7.12)
):
    result = {"item_id": item_id, "size": size}
    if q:
        result.update({"q": q})
    return result




# Multiple Parameters    and  add Body
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: int
    tax: Optional[float] = None
    
class User(BaseModel):
    username: str
    full_name: str = None
    
@app.put("/items_body/{item_id}")
async def update_item(
    *,
    item_id: Optional[int] = Path(..., title="theID of the item to get", gt=1, le=20),
    q: Optional[str] = "Test",
    item: Item,
    user: User,
    importance: int = Body(..., embed=True),
    importance2: int 
):
    results = {"item id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    if importance2:
        results.update({"importance2": importance2})
    if user:
        results.update({"user": user})
    if importance:
        results.update({"importance": importance})
    return results
