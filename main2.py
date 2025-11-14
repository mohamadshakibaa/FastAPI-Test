from fastapi import (
    Depends,
    FastAPI, 
    Query, 
    Path, 
    Body, 
    Cookie, 
    Header, 
    Form, 
    File, 
    UploadFile, 
    HTTPException,
    Request
)
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse
from typing import Optional, Literal, Union
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



class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

    
class UserIn2(UserBase):
    password: str


class UserOut2(UserBase):
    pass

    
class UserInDB(UserBase):
    hashed_password: str


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







# Union
class BaseItem(BaseModel):
    description: str
    type: str
    

class CarItem(BaseItem):
    type: Literal["car"] = "car"
    

class PlaneItem(BaseItem):
    type: Literal["plane"] = "plane"
    size: int
    

items2 = {
    "item1": {"description": "About beauty car", "type": "car"},
    "item2": {"description": "lab lab lab", "type": "plane", "size": 6},
}


@app.get("/item_union/{item_id}", response_model=Union[CarItem, PlaneItem])
async def read_item(item_id: Literal["item1", "item2"]):
    return items2[item_id]




# show in (get) List and Dict
class ListItem(BaseModel):
    name: str
    description: str
    

list_items = [
    {"name": "foo", "description": "There comes my hero"},
    {"name": "bar", "description": "hello baby"}
]

@app.get("/items_list/", response_model=list[ListItem])
async def show_list():
    return list_items

@app.get("/items_dict/", response_model=dict[str, float])
async def reat_dict():
    return {"name": 5, "description": 9}






# Form Fields
# this is good for HTML requests, but for using in (JSON) BODY is better
@app.post("/items_field/")
async def login(username: str = Form(...), password: str = Form(...)):
    print("password:", password)
    return {"username": username}





#About upload file
@app.post("/request_file")
async def get_file(file: bytes = File(...)):
    return len(file)


@app.post("/request_file2")
async def get_file_with_uploadfile(file: UploadFile):
    return file.filename


@app.post("/request_file3")
async def get_list_file(files: list[UploadFile] = File(..., description="many list")):
    return [file.filename for file in files]






# HTTPException 
items = {"foo": "the perfect"}


@app.get("/item_handeling_error/{item_name}")
async def handelling_error(item_name: str):
    if item_name not in items:
        raise HTTPException(
            status_code=404,
            detail="incorrect name",
            headers={"X-error": "hi"}, # it must be a Dict
        )
    return {"item": items[item_name]}




# Custom Exception + Handler
class UnicornException(Exception):
    def __init__(self, name):
        self.name = name
        
        
@app.exception_handler(UnicornException)
async def exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={
            "path": str(request.url),
            "method": request.method,
            "message": f"Nope! it not {exc.name}"
        }
    )
    

@app.get("/item_exception_handler/{item_id}")
async def watch_handler(item_id: int):
    if item_id == 99:
        raise UnicornException(name=item_id)
    return {"item_id": item_id}




# RequestValidationError
@app.exception_handler(RequestValidationError)
async def exception_handler3(request, exc):
    return PlainTextResponse(str(exc), status_code=400)


@app.get("/item_exception_handler2/{item_id}")
async def unicorn_exception_handler3(item_id: int):
    if item_id == 99:
        raise HTTPException(status_code=418, detail="Nope! i dont like 99")
    return {"item_id": item_id}





# Put & Patch
class Items4(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float = 30
    tax: float = 10
    tags: list[str] = []
    
items = {
    "foo": {"name": "foo", "description": "his name is foo", "price": 51},
    "bar": {"name": "bar", "description": "his name is bar", "tax": 60, "tags": []},
    "baz": {"name": "baz", "description": "his name is baz", "price": 17, "tags": ['as','as']}
}
    
    
@app.get("/items_get/{item_id}", response_model=Items4)
async def get_item(item_id: str):
    if item_id in items:
        return items.get(item_id)
    raise HTTPException(status_code=418, detail="Not exist")

@app.put("/items_put/{item_id}", response_model=Items4)
async def put_item(item_id: str, item: Items4):
    update_item_encoded = jsonable_encoder(item)
    items[item_id] = update_item_encoded
    return update_item_encoded
    
    
@app.patch("/items_patch/{item_id}", response_model=Items4)
def patch_item(item_id: str, item: Items4):
    stored_item_data = items.get(item_id)
    if stored_item_data is not None:
        stored_item_model = Items4(**stored_item_data)
    else:
        stored_item_model = Items4()
    update_data = item.dict(exclude_unset=True)
    update_item = stored_item_model.copy(update=update_data)
    items[item_id] = jsonable_encoder(update_item)
    print("update_item:", update_item)
    return update_item 
        
        






# Dependencies
fake_db_items = [{"item_id": "user1"}, {"item_id": "user2"}, {"item_id": "user3"}]


class CommenQuery:
    def __init__(self, q: str | None = None, skip: int = 2, limit: int = 10):
        self.q = q
        self.skip = skip
        self.limit = limit


# async def get_dependencies(q: str | None = None, skip: str = 1, limit: str = 10):
#     return {"q": q, "start": skip, "limit": limit}


@app.get("/item_depence")
async def get_user(de: CommenQuery = Depends()):
    response = {}
    if de.q:
        response.update({"q": de.q})
    items = fake_db_items[de.skip : de.skip + de.limit]
    response.update({"items": items})
    return response


