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


@fast_api_decorator(route="/sous/", method=["POST"])
def sous_function(x: str, a: str, b: str):
    return {f"{x} - {a} - {b} equals": int(x) - int(a) - int(b)}


# On "lance" les fonctions pour qu'elles soient lisibles par l'app FastAPI
power_function(x="0", a="0")
add_function(x="0", a="0")
sous_function(x="0", a="0", b="0")
