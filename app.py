import asyncio
from functools import lru_cache
from fastapi import FastAPI, APIRouter, Depends, HTTPException, Query, Request
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordRequestForm
from settings import Settings
from typing import Annotated
from Authentification import User, get_current_active_user, fake_users_db, UserInDB, fake_hash_password, \
    get_current_admin_user
from pydantic import BaseModel
import pickle
from collections import Counter
import os
import time

load_dotenv()
settings1 = Settings()

my_router = APIRouter()
app = FastAPI(title=settings1.title, description=settings1.description)
route_request_counter = Counter()
route_time_counter = Counter()


@app.on_event("shutdown")
def shutdown_event():
    """
    Remove the statistics file when the app shutdown
    """
    try:
        os.remove('saved_count.pkl')
    except Exception as e:
        print(f"Error deleting statistics file: {e}")


def get_saved_values():
    """
    Retrieve the statistics data saved in the file
    :return: dict with statistics values of all API routes
    """
    try:
        with open("saved_count.pkl", "rb") as file:
            values = pickle.load(file)
    except FileNotFoundError:
        with open('saved_count.pkl', 'wb') as file:
            values = dict()
            pickle.dump(values, file)
    return values


def save_value(values):
    """
    Save the current API statistics in a file
    :param values: dict with statistics values of all API routes
    """
    with open("saved_count.pkl", "wb") as file:
        pickle.dump(values, file)


@app.middleware("http")
async def count_requests(request: Request, call_next):
    """
    Increment the number of request by route and calculate the time while processing
    :param request: incoming HTTP request
    :param call_next: function that represents the next middleware or request handler in the processing pipeline
    :return: response of the API request
    """
    route = request.url.path
    route_request_counter[route] += 1
    start_time = time.time()
    response = await call_next(request)
    end_time = time.time()
    route_time_counter[route] += round(end_time - start_time, 6)
    return response


def check_args_type(dict_args, type_args):
    """
    Check if args in the dictionary corresponds to the expected type, raise an error if not
    :param dict_args: dict of arguments to check
    :param type_args: list of expected types
    """
    for value, expected_type in zip(dict_args.values(), type_args):
        if not isinstance(value, expected_type):
            raise TypeError(
                f"Type d'argument incorrect. Attendu : {expected_type.__name__}, Reçu : {type(value).__name__}"
            )


@lru_cache
def get_settings():
    return Settings()


def count_func_call(func):
    """
    Increment the number of call by fonction
    :param func: methode to increment the count
    """
    request_count = get_saved_values()
    key_func = func.__name__
    if key_func in request_count:
        request_count[key_func] += 1
    else:
        request_count[key_func] = 1
    save_value(request_count)


def fast_api_decorator(route, method, type_args):
    def decorator(func):
        def wrapper(**kwargs):
            # Handle argument type error
            check_args_type(dict_args=kwargs, type_args=type_args)
            # Count the number of request
            count_func_call(func=func)
            # add endpoint to the API
            my_router.add_api_route(path=route, endpoint=func, methods=method)
            app.include_router(my_router)
            return func(**kwargs)
        return wrapper
    return decorator


@fast_api_decorator(route="/power/", method=["GET"], type_args=[int, int])
def power_function(x: Annotated[int, Query(description="Int we'll compute the power")],
                   a: Annotated[int, Query(description="Power of the calculation")],
                   current_user: User = Depends(get_current_active_user)):
    return {f"{x} to the power of {a}": x ** a}


@fast_api_decorator(route="/add/", method=["GET"], type_args=[int, int])
def add_function(x: Annotated[int, Query(description="Int we'll add something")],
                 a: Annotated[int, Query(description="Int added")],
                 current_user: User = Depends(get_current_active_user)):
    return {f"{x} + {a} equals": x + a}


@fast_api_decorator(route="/sous/", method=["GET"], type_args=[int, list])
def sous_function(x: Annotated[int, Query(description="Int we'll substract something")],
                  lst: Annotated[list[int], Query(description="List of 2 int that will be substracted")],
                  current_user: User = Depends(get_current_active_user)):
    return {f"{x} - {lst[0]} - {lst[1]} equals": x - lst[0] - lst[1]}


class InputDiv(BaseModel):
    div: int


# Pour faire une requête avec un argument "Body" ou un json avec des arguments il faut passer
# par une méthode "POST" et pas "GET"
@fast_api_decorator(route="/div/", method=["POST"], type_args=[int, InputDiv])
def div_function(x: Annotated[int, Query(description="Int we will divide something")], item: InputDiv):
    return {f"{x} / {item.div} equals": item.div}


@app.get("/stats")
async def get_stats(current_user: User = Depends(get_current_admin_user)):
    avg_time = dict()
    for key in route_request_counter.keys():
        avg_time[key] = route_time_counter[key] * 1000 / route_request_counter[key]
    return {"Nombre d'appels aux fonctions décorées": get_saved_values(),
            "Nombre d'appels totaux des API par route": route_request_counter,
            "Temps moyen d'exécution par route en ms": avg_time}


@fast_api_decorator(route="/users/me", method=["GET"], type_args=[])
def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@fast_api_decorator(route="/rendement/", method=["POST"], type_args=[int, float])
def rendement(x: Annotated[int, Query(description="Int we'll add something")],
              r: Annotated[float, Query(description="float added")],
              current_user: User = Depends(get_current_active_user)):
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
async def info():
    return {
        "app_name": settings1.app_name,
        "admin_email": settings1.admin_email,
        "items_per_user": settings1.items_per_user,
    }


# On "lance" les fonctions pour qu'elles soient visibles par l'app FastAPI
read_users_me()
rendement(x=0, r=0.0)
power_function(x=0, a=0)
add_function(x=0, a=0)
sous_function(x=0, lst=[0, 0])
input_item = InputDiv(div=10)
div_function(x=100, item=input_item)
