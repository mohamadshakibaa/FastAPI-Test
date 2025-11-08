from fastapi import FastAPI, Query, Path, Body, Cookie, Header
from typing import Optional, Literal
from pydantic import BaseModel, Field, EmailStr
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
    
    
    
    
    
class ItemIn(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = 1.6
    tags: list[str] = []
    

class User(BaseModel):
    username: str
    full_name: str
    email: EmailStr

class UserIn(User):
    password: str
    
class UserOut(User):
    pass


@app.post("/items_response2", response_model= UserOut)
async def create_user(user: UserIn):
    return user

items = {
    "foo": {"name": "foo", "price": 15},
    "bar": {"name": "bar", "description": "hello my beauty", "price": 11},
    "baz": {"name": "baz", "tax": 11, "price": 30, "tags": ["water"]}
}


@app.get("/items1/{item_id}", response_model= ItemIn, response_model_include=["name", "description"])
async def read_item_name(item_id: Literal["foo", "bar", "baz"]):
    return items[item_id]


@app.get("/items2/{item_id}", response_model= ItemIn, response_model_exclude=["tax"])
async def read_item_name(item_id: Literal["foo", "bar", "baz"]):
    return items[item_id]


@app.get("/items3/{item_id}", response_model= ItemIn, response_model_exclude_unset=True)
async def read_item_name(item_id: Literal["foo", "bar", "baz"]):
    return items[item_id]






class UserIn2(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None

    
class UserOut2(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

    
class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_name: str | None = None


def fake_password_hasher(raw_password: str):
    return f'supersecret {raw_password}'


def fake_save_user(user_in: UserIn2):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("user_in.dict", user_in.dict())
    print("User saved")
    return user_in_db


@app.post("/hashed", response_model=UserOut2)
async def create_user(user_in: UserIn2):
    user_saved = fake_save_user(user_in)
    return user_saved


