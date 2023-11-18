"""
FastApiDecoratorBuilder

Description du Projet :
Votre défi dans le projet "FastApiDecoratorBuilder" est de concevoir un décorateur Python qui
transforme une fonction Python en une API FastAPI basée sur la fonction et des configurations
définies.

Objectifs du Projet :
- Création de Décorateur: Construire un décorateur qui transforme une fonction Python en API FastAPI.
- Gestion de Configurations: Implanter un mécanisme de configuration pour l’API.

Consignes :
1) Développement du Décorateur : Elaborez un décorateur qui, appliqué à une fonction, génère une API FastAPI
correspondante.
2) Configuration de l'API : Intégrez une méthode pour configurer les propriétés de l’API générée, telles que
les routes et les méthodes HTTP acceptées.
"""

# Use command : "python -m uvicorn main:app --reload" to lauch server and be able to request the "app" API.

from app import app, power_function, add_function, sous_function, rendement
import requests
import asyncio


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
    print(rendement(x=0, r=0.0))
    print(power_function(x=9, a=2))
    print(add_function(x=9, a=2))
    print(sous_function(x=9, lst=[2, 1]))
