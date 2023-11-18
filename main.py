from app import app, power_function, add_function, sous_function
import requests


def power(x, a):
    print(requests.get(f"http://127.0.0.1:8000/power/?x={x}&a={a}").json())


def add(x, a):
    print(requests.get(f"http://127.0.0.1:8000/add/?x={x}&a={a}").json())


def sous(x, lst):
    print(requests.get(f"http://127.0.0.1:8000/sous/?x={x}&lst={lst[0]}&lst={lst[1]}").json())


if __name__ == "__main__":
    power(x=9, a=2)
    add(x=9, a=2)
    sous(x=9, lst=[2, 1])
    print(power_function(x=9, a=2))
    print(add_function(x=9, a=2))
    print(sous_function(x=9, lst=[2, 1]))
