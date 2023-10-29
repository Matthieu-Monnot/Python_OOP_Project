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

from app import app, my_router, power_function
import requests


def power(x, a):
    print(requests.get(f"http://127.0.0.1:8000/power_function/{x}/{a}").json())


if __name__ == "__main__":
    power(x="9", a="2")
    # power_function(x="9", a="2")
    # print(requests.get("http://127.0.0.1:8000/power_function/10/2").json())
