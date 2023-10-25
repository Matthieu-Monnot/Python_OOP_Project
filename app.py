from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def index():
    return {"items": 1}


class CustomApp(FastAPI):
    def get_func_result(self, func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return result
        return wrapper


custom_app = CustomApp()


@custom_app.get_func_result("/")
def example():
    return {"items": 2}
