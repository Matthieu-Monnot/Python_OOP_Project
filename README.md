# FastApiDecoratorBuilder

"FastApiDecoratorBuilder" est un algorithme permettant de concevoir un décorateur Python qui transforme 
une fonction Python en une API FastAPI. 

## Installation

1. Télécharger les fichiers Python
2. Installer l'application FastAPI
   $ pip install fastapi
3. Installer le serveur ASGI
   $ pip install "uvicorn[standard]"
4. Lancer le serveur dans le terminal de l'application Python 
   $ python -m uvicorn main:app --reload
5. Le serveur API démarrera et sera accessible à l'adresse suivante : http://127.0.0.1:8000.
6. Un aperçu des requêtes implémentées est disponible à l'adresse suivante : http://127.0.0.1:8000/docs.

## Utilisation
Le décorateur 'fast_api_decorator' ajoute une route avec un endpoint correspondant aux paramètres de la requête 
(paramètres de la fonction). Le décorateur appliqué à une fonction puis exécutée sur le même script de l'instance 
FastAPI (app) permet de rendre utilisable l'API avec une route qui dépend de la fonction et de ses propres paramètres. 
Ainsi, une fois cette étape réalisée, il est possible de requêter l'API de la fonction à laquelle on a appliqué le
décorateur avec n'importe quels arguments. La réponse de l'API est évidemment l'output de cette fonction. 
L'API est configurée directement grâce aux paramètres du décorateur avec les routes (ex: "/power/", "/add/" ou "/sous/"),
les méthodes HTTP (ex: "GET", "POST", "PUT", "DELETE") et une liste de type correspondants aux types des arguments de la
fonction décorée.

## Test
Dans le code suivant, il y a trois fonctions qui ont été implémenté dans l'API. Il suffit d'entrer les points de 
terminaison suivants après le lien 'http://127.0.0.1:8000'.

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
     -  'x': Nombre à soustraire (integer)
     -  [a, b] : liste de nombre (List[int])
   
   Exemple : '/sous/?x=10&lst=3&lst=2' pour soustraire 3 et 2 à 10


## Compte rendu du projet

Dans FastAPI, les routes doivent être enregistrées auprès de l'instance d'application pour qu'elles soient 
accessibles lorsque le serveur est en cours d'exécution. Dans notre code, les routes sont définies à l'aide de 
décorateurs qui configurent essentiellement le comportement de routage. Cependant, jusqu'à ce qu'on invoque 
les fonctions décorées avec le décorateur @fast_api_decorator, les routes ne sont pas ajoutées à l'application 
FastAPI. En effet, lors du lancement de l'application, le programme app.py est exécuté mais les routes ne sont pas 
ajoutées tant que le décorateur n'est pas appelé, c'est-à-dire que les fonctions décorées ne sont pas exécutées une
première fois. Il est alors nécessaire d'appeler chaque fonction dans le programme app afin de rendre utilisable
leur route.
