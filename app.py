from fastapi import FastAPI, APIRouter, Query
from typing import Annotated
from pydantic import BaseModel


my_router = APIRouter()
app = FastAPI()
request_count = 0


def fast_api_decorator(route, method, type_args):
    def decorator(func):
        def wrapper(**kwargs):
            # Handle argument type error
            for value, expected_type in zip(kwargs.values(), type_args):
                if not isinstance(value, expected_type):
                    raise TypeError(f"Type d'argument incorrect. Attendu : {expected_type.__name__}, Reçu : {type(value).__name__}")

            # Count the number of request
            global request_count
            request_count += 1

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
    global request_count
    return {"request_count": request_count}


# On "lance" les fonctions pour qu'elles soient lisibles par l'app FastAPI
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