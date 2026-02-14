from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel


app = FastAPI()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

fake_users_db = {
    "johndoo": dict(
        username="johndoo",
        full_name="Johndoo",
        email="johndoo@gmail.com",
        hashed_password="123456",
        disable=False,
    ),
    "alice": dict(
        username="alice",
        full_name="Alice",
        email="alice@gmail.com",
        hashed_password="123456",
        disable=True,
    ),
}


def fake_hashed_password(password: str):
    return f"{password}"


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disable: bool | None = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_encode_token(token):
    return get_user(fake_users_db, token)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_encode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disable:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="incoorect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hashed_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect password or username")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def get_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/users")
async def read_user(token: str = Depends(oauth2_scheme)):
    return {"token": token}
