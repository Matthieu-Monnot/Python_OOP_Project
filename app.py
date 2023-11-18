from typing import Annotated
from functools import lru_cache
from fastapi import FastAPI, APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from Authentification import User, get_current_active_user, fake_users_db, UserInDB, fake_hash_password, \
    get_current_inactive_user


from settings import Settings


my_router = APIRouter()
app = FastAPI()


@lru_cache
def get_settings():
    return Settings()


@app.get("/info")
async def info(settings: Annotated[Settings, Depends(get_settings)]):
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
    }






# @app.get("/info")
# async def info():
#     return {
#         "app_name": settings.app_name,
#         "admin_email": settings.admin_email,
#         "items_per_user": settings.items_per_user,
#     }

# class Settings(BaseSettings):
#     DEFAULT_VAR: str = "some default string value"  # default value if env variable does not exist
#     API_KEY: str = "ma key"
#     APP_MAX: int = 100  # default value if env variable does not exist
#
#     model_config = SettingsConfigDict(env_file=".env")



#def get_settings():
#    return Settings()


# async def info(settings: Settings = Depends(get_settings)):
#     return {
#         "default variable": settings.DEFAULT_VAR,
#         "api key": settings.API_KEY,
#         "app max integer": settings.APP_MAX,
#     }
#
# @app.get("/")
# @app.get("/env")
# async def root():
#      return {"settings": settings}

def fast_api_decorator(route, method):
    def decorator(func):
        def wrapper(*args, **kwargs):
            #if current_user in kwargs.values():
            my_router.add_api_route(path=route, endpoint=func, methods=method)
            app.include_router(my_router)
            return func(*args, **kwargs)
        return wrapper
    return decorator



@fast_api_decorator(route="/add/", method=["GET"])
def add_function(x: str, a: str):
    return {f"{x} + {a} equals": int(x) + int(a)}

@fast_api_decorator(route="/sous/", method=["GET"])
def sous_function(x: str, lst):
    return {f"{x} - {lst[0]} - {lst[1]} equals": int(x) - int(lst[0]) - int(lst[1])}



@fast_api_decorator(route="/users/me", method=["GET"])
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@fast_api_decorator(route="/power/", method=["POST"])
async def power_function(x: float, a: float, current_user: User = Depends(get_current_inactive_user)):
    return {f"{x} to the power of {a}": float(x)**float(a)}

@fast_api_decorator(route="/rendement/", method=["POST"])
async def rendement(x: int, r: float, current_user: User = Depends(get_current_active_user)):
    return {f"{x} * (1 + {r}) equals": int(x) * (1 + float(r))}

@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}




# On "lance" les fonctions pour qu'elles soient visibles par l'app FastAPI
read_users_me()
rendement(x="0", r="0")
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