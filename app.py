from fastapi import FastAPI, APIRouter, Query, Request
from typing import Annotated
from pydantic import BaseModel
import pickle
from collections import Counter

my_router = APIRouter()
app = FastAPI()


def get_saved_value():
    try:
        with open("saved_count.pkl", "rb") as file:
            values = pickle.load(file)
    except FileNotFoundError:
        with open("saved_count.pkl", 'wb') as file:
            values = {"power_function": 0, "add_function": 0, "sous_function": 0, "div_function": 0}
            pickle.dump(values, file)
    return values


request_count = get_saved_value()


def save_value(values):
    with open("saved_count.pkl", "wb") as file:
        pickle.dump(values, file)


route_request_counter = Counter()


@app.middleware("http")
async def count_requests(request: Request, call_next):
    route = request.url.path
    route_request_counter[route] += 1
    response = await call_next(request)
    return response


def fast_api_decorator(route, method, type_args):
    def decorator(func):
        def wrapper(**kwargs):
            # Handle argument type error
            for value, expected_type in zip(kwargs.values(), type_args):
                if not isinstance(value, expected_type):
                    raise TypeError(f"Type d'argument incorrect. Attendu : {expected_type.__name__}, Reçu : {type(value).__name__}")

            # Count the number of request
            request_count = get_saved_value()
            request_count[func.__name__] += 1
            save_value(request_count)

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
    return {"Nombre d'appels aux fonctions décorées" : get_saved_value(),
            "Nombre d'appels totaux des API par route" : route_request_counter}


# On "lance" les fonctions pour qu'elles soient lisibles par l'app FastAPI
power_function(x=0, a=0)
add_function(x=0, a=0)
sous_function(x=0, lst=[0, 0])
input_item = InputDiv(div=10)
div_function(x=100, item=input_item)
