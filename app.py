from fastapi import FastAPI, APIRouter, Depends, HTTPException, Query, Request
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordRequestForm
from settings import Settings
from typing import Annotated
from Authentification import User, get_current_active_user, fake_users_db, UserInDB, fake_hash_password, \
    get_current_admin_user, get_current_user
from pydantic import BaseModel
import pickle
from collections import Counter
import os
import time

# Load environment variables from a .env file if present
load_dotenv()
# Create an instance of the Settings class to load environment variables
sett_Env = Settings()

my_router = APIRouter()
app = FastAPI(title=sett_Env.title, description=sett_Env.description)
route_request_counter = Counter()
route_time_counter = Counter()


@app.on_event("shutdown")
def shutdown_event():
    """
    Remove the statistics file when the app shutdown
    """
    try:
        os.remove('saved_count.pkl')
    except Exception as e:
        print(f"Error deleting statistics file: {e}")


def get_saved_values():
    """
    Retrieve the statistics data saved in the file
    :return: dict with statistics values of all API routes
    """
    try:
        with open("saved_count.pkl", "rb") as file:
            values = pickle.load(file)
    except FileNotFoundError:
        with open('saved_count.pkl', 'wb') as file:
            values = dict()
            pickle.dump(values, file)
    return values


def save_value(values):
    """
    Save the current API statistics in a file
    :param values: dict with statistics values of all API routes
    """
    with open("saved_count.pkl", "wb") as file:
        pickle.dump(values, file)


@app.middleware("http")
async def count_requests(request: Request, call_next):
    """
    Increment the number of request by route and calculate the time while processing
    :param request: incoming HTTP request
    :param call_next: function that represents the next middleware or request handler in the processing pipeline
    :return: response of the API request
    """
    route = request.url.path
    route_request_counter[route] += 1
    start_time = time.time()
    response = await call_next(request)
    end_time = time.time()
    route_time_counter[route] += round(end_time - start_time, 6)
    return response


def check_args_type(dict_args, type_args):
    """
    Check if args in the dictionary corresponds to the expected type, raise an error if not
    :param dict_args: dict of arguments to check
    :param type_args: list of expected types
    """
    for value, expected_type in zip(dict_args.values(), type_args):
        if not isinstance(value, expected_type):
            raise TypeError(
                f"Type d'argument incorrect. Attendu : {expected_type.__name__}, Reçu : {type(value).__name__}"
            )


def count_func_call(func):
    """
    Increment the number of call by fonction
    :param func: methode to increment the count
    """
    request_count = get_saved_values()
    key_func = func.__name__
    if key_func in request_count:
        request_count[key_func] += 1
    else:
        request_count[key_func] = 1
    save_value(request_count)


def fast_api_decorator(route, method, type_args):
    def decorator(func):
        def wrapper(**kwargs):
            # Handle argument type error
            check_args_type(dict_args=kwargs, type_args=type_args)
            # Count the number of request
            count_func_call(func=func)
            # add endpoint to the API
            my_router.add_api_route(path=route, endpoint=func, methods=method)
            app.include_router(my_router)
            return func(**kwargs)
        return wrapper
    return decorator


@fast_api_decorator(route="/power/", method=["GET"], type_args=[int, int])
def power_function(x: Annotated[int, Query(description="Int we'll compute the power")],
                   a: Annotated[int, Query(description="Power of the calculation")],
                   current_user: User = Depends(get_current_active_user)):
    """
    Calculates the power of a given number.
    :param x: The base number
    :param a: The power to raise the base number to.
    :param current_user: The current user.
    :return: The result of the power calculation.
    """
    return {f"{x} to the power of {a}": x ** a}


@fast_api_decorator(route="/add/", method=["GET"], type_args=[int, int])
def add_function(x: Annotated[int, Query(description="Int we'll add something")],
                 a: Annotated[int, Query(description="Int added")],
                 current_user: User = Depends(get_current_active_user)):
    """
    Adds two numbers.
    :param x:The first number.
    :param a:The second number to add.
    :param current_user: The current user.
    :return:The result of the addition.
    """
    return {f"{x} + {a} equals": x + a}


@fast_api_decorator(route="/sous/", method=["GET"], type_args=[int, list])
def sous_function(x: Annotated[int, Query(description="Int we'll substract something")],
                  lst: Annotated[list[int], Query(description="List of 2 int that will be substracted")],
                  current_user: User = Depends(get_current_active_user)):
    """
    Subtracts two numbers.
    :param x:The first number.
    :param lst: The list containing two numbers to subtract from the first.
    :param current_user: The current user.
    :return: The result of the subtraction.
    """
    return {f"{x} - {lst[0]} - {lst[1]} equals": x - lst[0] - lst[1]}


class InputDiv(BaseModel):
    div: int


# Pour faire une requête avec un argument "Body" ou un json avec des arguments il faut passer
# par une méthode "POST" et pas "GET"
@fast_api_decorator(route="/div/", method=["POST"], type_args=[int, InputDiv])
def div_function(x: Annotated[int, Query(description="Int we will divide something")], item: InputDiv,
                 current_user: User = Depends(get_current_active_user)):
    """
    Divides two numbers.
    :param x: The numerator.
    :param item: The Pydantic model containing the divisor.
    :param current_user: The current user.
    :return: The result of the division.
    """
    return {f"{x} / {item.div} equals": item.div}


@app.get("/stats")
async def get_stats(current_user: User = Depends(get_current_admin_user)):
    """
    Get statistics about API usage.
    :param current_user: The current admin user.
    :return: Statistics including the number of API calls per route and average execution time.
    """
    avg_time = dict()
    for key in route_request_counter.keys():
        avg_time[key] = route_time_counter[key] * 1000 / route_request_counter[key]
    return {"Nombre d'appels aux fonctions décorées": get_saved_values(),
            "Nombre d'appels totaux des API par route": route_request_counter,
            "Temps moyen d'exécution par route en ms": avg_time}


@fast_api_decorator(route="/users/me", method=["GET"], type_args=[])
def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Get information about the current user.
    :param current_user: The current user.
    :return:Information about the current user.
    """
    return current_user


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    Log in and retrieve an access token.

    :param form_data: The OAuth2 password request form containing username and password.
    :return: The access token and token type.
    """
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": user.username, "token_type": "bearer"}


@fast_api_decorator(route="/info/me", method=["GET"], type_args=[])
async def info():
    """
    Get information about the application.

    :return: Information about the application.
    """
    return {
        "API_name": sett_Env.title,
        "API_description": sett_Env.description,
        "API_url": sett_Env.url,
        "admin_email": sett_Env.admin_email,
        "command_to_load": sett_Env.command_load
    }


# On "lance" les fonctions pour qu'elles soient visibles par l'app FastAPI
read_users_me()
info()
power_function(x=0, a=0)
add_function(x=0, a=0)
sous_function(x=0, lst=[0, 0])
input_item = InputDiv(div=10)
div_function(x=100, item=input_item)

