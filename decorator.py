# In this script we build the decorator and the function we want to transform into an API
from app import app


def fast_api_decorator(route, methods):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print("before func")
            func(*args, **kwargs)
            print("after func")
            return func(*args, **kwargs)

        # add root and function return to the API
        app.add_api_route(route, wrapper, methods=methods)
        return wrapper
    return decorator


@fast_api_decorator(route="/power", methods=["GET"])
def power_function(x, a):
    return {f"{x} to the power of {a}": x**a}
