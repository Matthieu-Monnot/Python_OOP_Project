from fastapi import FastAPI, APIRouter, Query, Request
from typing import Annotated
from pydantic import BaseModel
import pickle
from collections import Counter
import os
import time

my_router = APIRouter()
app = FastAPI()
route_request_counter = Counter()
route_time_counter = Counter()


@app.on_event("shutdown")
def shutdown_event():
    try:
        os.remove('saved_count.pkl')
    except Exception as e:
        print(f"Error deleting statistics file: {e}")


def get_saved_values():
    try:
        with open("saved_count.pkl", "rb") as file:
            values = pickle.load(file)
    except FileNotFoundError:
        with open('saved_count.pkl', 'wb') as file:
            values = dict()
            pickle.dump(values, file)
    return values


def save_value(values):
    with open("saved_count.pkl", "wb") as file:
        pickle.dump(values, file)


@app.middleware("http")
async def count_requests(request: Request, call_next):
    route = request.url.path
    route_request_counter[route] += 1
    start_time = time.time()
    response = await call_next(request)
    end_time = time.time()
    route_time_counter[route] += end_time - start_time
    return response


def check_args_type(dict_args, type_args):
    for value, expected_type in zip(dict_args.values(), type_args):
        if not isinstance(value, expected_type):
            raise TypeError(f"Type d'argument incorrect. Attendu : {expected_type.__name__}, Reçu : {type(value).__name__}")


def count_func_call(func):
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
def power_function(x: Annotated[int, Query(description="Int we'll compute the power")], a: Annotated[int, Query(description="Power of the calculation")]):
    return {f"{x} to the power of {a}": x ** a}


@fast_api_decorator(route="/add/", method=["GET"], type_args=[int, int])
def add_function(x: Annotated[int, Query(description="Int we'll add something")], a: Annotated[int, Query(description="Int added")]):
    return {f"{x} + {a} equals": x + a}


@fast_api_decorator(route="/sous/", method=["GET"], type_args=[int, list])
def sous_function(x: Annotated[int, Query(description="Int we'll substract something")], lst: Annotated[list[int], Query(description="List of 2 int that will be substracted")]):
    return {f"{x} - {lst[0]} - {lst[1]} equals": x - lst[0] - lst[1]}


class InputDiv(BaseModel):
    div: int


# Pour faire une requête avec un argument "Body" ou un json avec des arguments il faut passer
# par une méthode "POST" et pas "GET"
@fast_api_decorator(route="/div/", method=["POST"], type_args=[int, InputDiv])
def div_function(x: Annotated[int, Query(description="Int we will divide something")], item: InputDiv):
    return {f"{x} / {item.div} equals": item.div}


@app.get("/stats")
async def get_stats():
    avg_time = dict()
    for key in route_request_counter.keys():
        avg_time[key] = route_time_counter[key] * 1000 / route_request_counter[key]
    return {"Nombre d'appels aux fonctions décorées": get_saved_values(),
            "Nombre d'appels totaux des API par route": route_request_counter,
            "Temps moyen d'exécution par route en ms": avg_time}


# On "lance" les fonctions pour qu'elles soient lisibles par l'app FastAPI
power_function(x=0, a=0)
add_function(x=0, a=0)
sous_function(x=0, lst=[0, 0])
input_item = InputDiv(div=10)
div_function(x=100, item=input_item)
