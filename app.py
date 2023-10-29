from fastapi import FastAPI, APIRouter

my_router = APIRouter()
app = FastAPI()

"""
def square_function(x: str):
    return {f"{x} square equals": int(x)**2}


def power_function(x: str, a: str):
    return {f"{x} to the power of {a}": int(x)**int(a)}


route_path = '/power_function/{x}/{a}'
my_router.add_api_route(route_path, endpoint=power_function)
app.include_router(my_router)

"""


def fast_api_decorator(func):
    def wrapper(x, a):
        my_router.add_api_route(path='/{func}/{x}/{a}', endpoint=func)
        app.include_router(my_router)
    return wrapper


@fast_api_decorator
def power_function(x: str, a: str):
    return {f"{x} to the power of {a}": int(x)**int(a)}


power_function(x=0, a=0)
