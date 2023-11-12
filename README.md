# FastApiDecoratorBuilder

"FastApiDecoratorBuilder" est un algorithme permettant de concevoir un décorateur Python qui transforme une fonction Python en une API FastAPI. 

## Installation

1. Télécharger les fichiers Python
2. Installer l'application FastAPI
   $ pip install fastapi
3. Installer le serveur ASGI
   $ pip install "uvicorn[standard]"
4. Lancer le serveur dans le terminal de l'application Python 
   $ python -m uvicorn main:app --reload
5. Le serveur API démarrera et sera accessible à http://127.0.0.1:8000.

## Utilisation
Le décorateur 'fast_api_decorator' ajoute une route avec un endpoint correspondant aux paramètres de la requête (paramètres de la fonction). Le décorateur appliqué à une fonction puis "lancée" sur le même script de l'instance FastAPI (app) permet de requêter l'API avec une route qui dépend de la fonction et de ses propres paramètres. 
L'API est configurée directement grâce aux paramètres du décorateur avec les routes ("/power/", "/add/" et "/sous/") et les méthodes HTTP ("GET", "POST", "PUT", "DELETE").

## Test
Dans le code suivant, il y a trois fonctions qui ont été implémenté dans l'API. Il suffit d'entrer les points de terminaison suivants après le lien 'http://127.0.0.1:8000'.

1. Power
   Description : Calcul de la puissance d'un nombre
   Paramètres :
     -  'x': Nombre (integer)
     -  'a': La puissance (integer)
   
   Exemple : '/power/?x=2&a=3' retournera le résultat de 2 à la puissance 3

2. Add
   Description : Calcul l'addition de deux nombres
   Paramètres :
     -  'x': Nombre (integer)
     -  'a': Nombre (integer)
   
   Exemple : '/add/?x=2&a=3' retournera la somme de 2 et 3

3. Sous
   Description : Calcul la soustraction de trois nombres
   Paramètres :
     -  'x': Nombre à soustraire(integer)
     -  'a': Nombre (integer)
     -  'b': Nombre (integer)
   
   Exemple : '/sous/?x=10&a=3&b=2' pour soustraire 3 et 2 à 10



   
