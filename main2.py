from fastapi import FastAPI, Query, Path, Body, Cookie, Header
from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime, time, timedelta


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





# UUID
# you must set uuid in the terminal => 
#  import uuid 
#  from uuid import uuid4
#  uuid4()
@app.put("/items_uuid/{item_id}")
async def update_item(
    item_id: UUID,
    start_date: Optional[datetime] = Body(None),
    end_time: Optional[datetime] = Body(None),
    repeat_at: Optional[time] = Body(None),
    process_after: Optional[timedelta] = Body(None)
):
    start_process = start_date + process_after
    duration = end_time - start_process
    return {"item_id": item_id,
            "start_date": start_date,
            "end_time": end_time,
            "repeat_at": repeat_at,
            "process_after": process_after,
            "start_process": start_process,
            "duration": duration
}






@app.get("/item_cookie")
async def get_cookie(
    cookie: Optional[str] = Cookie(None),
    accept_encoding: Optional[str] = Header(None, convert_underscores=False),
    sec_ch_ua: Optional[str] = Header(None),
    user_agent: Optional[str] = Header(None)
):
    return {
        "cookie": cookie,
        "accept_encoding": accept_encoding,
        "sec_ch_ua": sec_ch_ua,
        "user_agent": user_agent

}