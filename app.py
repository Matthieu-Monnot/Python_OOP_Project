import asyncio
from typing import Annotated
from functools import lru_cache
from fastapi import FastAPI, APIRouter, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordRequestForm
from Authentification import User, get_current_active_user, fake_users_db, UserInDB, fake_hash_password, \
    get_current_inactive_user
from pydantic import BaseModel

from settings import Settings


my_router = APIRouter()
app = FastAPI()


@lru_cache
def get_settings():
    return Settings()

def get_saved_value():
    try:
        with open("saved_count.txt", "r") as file:
            value = int(file.read())
    except FileNotFoundError:
        with open("saved_count.txt", 'w') as file:
            file.write('0')
            value = 0
    return value


request_count = get_saved_value()


def save_value(value):
    with open("saved_count.txt", "w") as file:
        file.write(str(value))


# def fast_api_decorator(route, method):
#     def decorator(func):
#         def wrapper(*args, **kwargs):
#             #if current_user in kwargs.values():
#             my_router.add_api_route(path=route, endpoint=func, methods=method)
#             app.include_router(my_router)
#             return func(*args, **kwargs)
#         return wrapper
#     return decorator

def fast_api_decorator(route, method, type_args):
    def decorator(func):
        def wrapper(**kwargs):
            # Handle argument type error if type_args is not None
            if type_args is not None:
                for value, expected_type in zip(kwargs.values(), type_args):
                    if not isinstance(value, expected_type):
                        raise TypeError(f"Type d'argument incorrect. Attendu : {expected_type.__name__}, Reçu : {type(value).__name__}")

            # Count the number of request
            global request_count
            request_count += 1
            save_value(request_count)

            # add endpoint to the API
            my_router.add_api_route(path=route, endpoint=func, methods=method)
            app.include_router(my_router)
            return func(**kwargs)
        return wrapper
    return decorator


@fast_api_decorator(route="/add/", method=["GET"], type_args=[int, int])
def add_function(x: Annotated[int, Query(description="Int we'll add something")], a: Annotated[int, Query(description="Int added")]):
    return {f"{x} + {a} equals": x + a}

@fast_api_decorator(route="/sous/", method=["GET"], type_args=[int, list])
def sous_function(x: Annotated[int, Query(description="Int we'll substract something")], lst: Annotated[list[int], Query(description="List of 2 int that will be substracted")]):
    return {f"{x} - {lst[0]} - {lst[1]} equals": x - lst[0] - lst[1]}



@fast_api_decorator(route="/users/me", method=["GET"],type_args=None)
def read_users_me(current_user: User = Depends(get_current_active_user)):
      return current_user

@fast_api_decorator(route="/power/", method=["POST"],type_args=[int, int])
def power_function(x: Annotated[int, Query(description="Int we'll add something")], a: Annotated[int, Query(description="Int added")], current_user: User = Depends(get_current_inactive_user)):
    return {f"{x} to the power of {a}": int(x)**int(a)}

@fast_api_decorator(route="/rendement/", method=["POST"],type_args=[int, float])
def rendement(x: Annotated[int, Query(description="Int we'll add something")], r: Annotated[float, Query(description="float added")], current_user: User = Depends(get_current_active_user)):
     return {f"{x} * (1 + {r}) equals": int(x) * (1 + float(r))}

@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/info")
async def info(settings: Annotated[Settings, Depends(get_settings)]):
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
    }


class InputDiv(BaseModel):
    div: int


# Pour faire une requête avec un argument "Body" ou un json avec des arguments il faut passer
# par une méthode "POST" et pas "GET"
@fast_api_decorator(route="/div/", method=["POST"], type_args=[int, InputDiv])
def div_function(x: Annotated[int, Query(description="Int we will divide something")], item: InputDiv):
    return {f"{x} / {item.div} equals": item.div}


@app.get("/stats")
async def get_stats():
    request_count = get_saved_value()
    return {"request_count": request_count}


# On "lance" les fonctions pour qu'elles soient visibles par l'app FastAPI
read_users_me()
rendement(x=0, r=0.0)
power_function(x=0, a=0)
add_function(x=0, a=0)
sous_function(x=0, lst=[0, 0])
input_item = InputDiv(div=10)
div_function(x=100, item=input_item)

# résolution pb de lancement des fonctions
"""
from fastapi import FastAPI, APIRouter

app = FastAPI()

class PowerEndpoint:
    router = APIRouter()

    @router.get("/power/")
    async def power_function(self, x: str, a: str):
        return {f"{x} to the power of {a}": int(x)**int(a)}

class AddEndpoint:
    router = APIRouter()

    @router.get("/add/")
    async def add_function(self, x: str, a: str):
        return {f"{x} + {a} equals": int(x) + int(a)}

class SousEndpoint:
    router = APIRouter()

    @router.get("/sous/")
    async def sous_function(self, x: str, lst):
        return {f"{x} - {lst[0]} - {lst[1]} equals": int(x) - int(lst[0]) - int(lst[1])}

# Including the routers directly in the main app
app.include_router(PowerEndpoint.router, tags=["power"])
app.include_router(AddEndpoint.router, tags=["add"])
app.include_router(SousEndpoint.router, tags=["sous"])
"""