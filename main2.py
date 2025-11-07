from fastapi import FastAPI, Query, Path, Body
from typing import Optional
from pydantic import BaseModel, Field


app = FastAPI()


# Field just like Body and Path
class Item(BaseModel):
    name: str
    description: str = Field(None, description="test for field")
    price: int = Field(..., title="the price must be greater then zero.")
    tax: float = Field(None, description="this is tax of price")


@app.put("/items/{item_id}")
async def update_item(
    item_id: int = Path(..., description="hello"), item: Item = Body(...)
):
    result = {"item_id": item_id, "item": item}
    return result







# second port of 3 ports that you show to swagger EXAMPLE for each item
class Item2(BaseModel):
    name: str = Field(..., example="foo")
    description: Optional[str] = Field(None, example="a very good item")
    price: int = Field(..., example=19)
    tax: Optional[float] = Field(None, example=1.5)


@app.put("/items_ex/{item_id}")
async def update_item(item_id: int, item: Item2):
    result = {"item_id": item_id, "item": item}
    return result