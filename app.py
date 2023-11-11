from fastapi import FastAPI, APIRouter


my_router = APIRouter()
app = FastAPI()


def fast_api_decorator(route, method):
    def decorator(func):
        def wrapper(*args, **kwargs):
            my_router.add_api_route(path=route, endpoint=func, methods=method)
            app.include_router(my_router)
            return func(*args, **kwargs)
        return wrapper
    return decorator


@fast_api_decorator(route="/power/", method=["GET"])
def power_function(x: str, a: str):
    return {f"{x} to the power of {a}": int(x)**int(a)}


@fast_api_decorator(route="/add/", method=["GET"])
def add_function(x: str, a: str):
    return {f"{x} + {a} equals": int(x) + int(a)}


@fast_api_decorator(route="/sous/", method=["GET"])
def sous_function(x: str, lst):
    return {f"{x} - {lst[0]} - {lst[1]} equals": int(x) - int(lst[0]) - int(lst[1])}


# On "lance" les fonctions pour qu'elles soient lisibles par l'app FastAPI
power_function(x="0", a="0")
add_function(x="0", a="0")
sous_function(x="0", lst=[0, 0])

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