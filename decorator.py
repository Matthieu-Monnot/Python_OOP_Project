# In this script we build the decorator and the function we want to transform into an API
from app import app, my_router


def fast_api_decorator(route):
    def decorator(func):
        def wrapper(x, a):
            func(x, a)
            return func(x, a)
        my_router.add_api_route(path='/{func}/{x}/{a}', endpoint=wrapper)
        app.include_router(my_router)
        return wrapper
    return decorator


@fast_api_decorator(route="")
def power_function(x, a):
    return {f"{x} to the power of {a}": x**a}
