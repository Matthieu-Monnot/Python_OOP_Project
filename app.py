import time

from fastapi import FastAPI, APIRouter
from functools import wraps

import ast

my_router = APIRouter()
app = FastAPI()

def rate_limiting(max_calls: int, time_frame: int):
    def decorator(func):
        calls = []

        @wraps(func)
        async def wrapper(*args, **kwargs):
            now = time.time()
            call_in_time_frame = [call for call in calls if call > now - time_frame]
            if len(call_in_time_frame) >= max_calls:
                raise print("rate limit exceeded")
            calls.append(now)
            return await func(*args, **kwargs)

        return wrapper

    return decorator


def fast_api_decorator(route, method, type_args):
    def decorator(func):
        def wrapper(**kwargs):
            # Handle argument type error
            for value, expected_type in zip(kwargs.values(), type_args):
                if not isinstance(value, expected_type):
                    raise TypeError(
                        f"Type d'argument incorrect. Attendu : {expected_type.__name__}, Reçu : {type(value).__name__}")

            # add endpoint to the API
            my_router.add_api_route(path=route, endpoint=func, methods=method)
            app.include_router(my_router)
            return func(**kwargs)

        return wrapper

    return decorator


@fast_api_decorator(route="/power/", method=["GET"], type_args=[str, str])
@rate_limiting(max_calls=10, time_frame=60)
def power_function(x: str, a: str):
    return {f"{x} to the power of {a}": int(x) ** int(a)}


@fast_api_decorator(route="/add/", method=["GET"], type_args=[str, str])
def add_function(x: str, a: str):
    return {f"{x} + {a} equals": int(x) + int(a)}


@fast_api_decorator(route="/sous/", method=["GET"], type_args=[str, list])
def sous_function(x, lst):
    x = ast.literal_eval(x)
    lst = ast.literal_eval(lst)
    return {f"{x} - {lst[0]} - {lst[1]} equals": x - lst[0] - lst[1]}


# On "lance" les fonctions pour qu'elles soient lisibles par l'app FastAPI
power_function(x="2", a="3")
# add_function(x="0", a="0")
# ous_function(x="0", lst=[0, 0])

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
