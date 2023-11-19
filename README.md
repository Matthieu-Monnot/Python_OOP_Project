# FastApi Decorator Builder

"FastApi Decorator Builder" est un algorithme permettant de concevoir un décorateur Python qui transforme 
une fonction Python en une API FastAPI. Les fonctionnalités sont accessible suivant une authentification. 
L'API permet de collecter des données statisques. 

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
1. Le décorateur
Le décorateur 'fast_api_decorator' ajoute une route avec un endpoint correspondant aux paramètres de la requête 
(paramètres de la fonction). Le décorateur appliqué à une fonction puis exécutée sur le même script de l'instance 
FastAPI (app) permet de rendre utilisable l'API avec une route qui dépend de la fonction et de ses propres paramètres. 
Ainsi, une fois cette étape réalisée, il est possible de requêter l'API de la fonction à laquelle on a appliqué le
décorateur avec n'importe quels arguments. La réponse de l'API est évidemment l'output de cette fonction. 
L'API est configurée directement grâce aux paramètres du décorateur avec les routes (ex: "/power/", "/add/" ou "/sous/"),
les méthodes HTTP (ex: "GET", "POST", "PUT", "DELETE") et une liste de type correspondants aux types des arguments de la
fonction décorée.


2. L'authentification
Cet API utilise une authentification OAuth2 Password Bearer pour assurer la sécurité des endpoints. 
Trois types d'utilisateurs sont définis: administrateur (username : "admin" & password : "secret"), utilisateur régulier 
(username : "bod" & password : "secret1") et utilisateur inactif (username : "alice" & password : "secret2"). 
L'administrateur a accès à toutes les fonctionnalitées proposées par l'API dont les statistiques. 
L'utilisateur actif peut utiliser les fonctions mathématiques alors que l'utilisateur inactif ne peut qu'accèder qu'à la 
fonctionnalité 'info' de l'API. 
Si un token invalide ou si une fonctionnalité réservée à un type d'utilisateur spécifique est renseigné 
sans les permissions nécessaires, l'API renverra une erreur : 
   - 401 Unauthorized: Le token fourni est invalide.
   - 400 Bad Request: Vous n'avez pas les permissions nécessaires pour accéder à cette fonctionnalité.


3. Suivi des Statistiques
Les informations telles que le nombre d'appels par route, le temps moyen d'exécution par route sont collectées 
automatiquement à chaque appel d'API. -> enregistré dans un fichier .pki

## Fonctionnalités
Dans le code suivant, il y a plusieurs fonctions qui ont été implémenté dans l'API. Certaines fonctions nécéssitent des authentifications.

### Information API
   Info
   Description : Obtenir des informations sur l'API
   Route: '/info/' 
   Accès : Pas d'accès spécifique

### Opérations Mathématiques
1. Power
   Description : Calcul de la puissance d'un nombre
   Route: '/power/'
   Accès via : Un token d'authentification
   Paramètres :
     -  'x': Nombre (integer)
     -  'a': La puissance (integer)


2. Add
   Description : Calcul l'addition de deux nombres
   Route: '/add/'
   Accès via : Un token d'authentification
   Paramètres :
     -  'x': Nombre (integer)
     -  'a': Nombre (integer)


3. Sous
   Description : Calcul la soustraction de trois nombres
   Route: '/sous/'
   Accès via : Un token d'authentification
   Paramètres :
     -  'x': Nombre à soustraire (integer)
     -  [a, b] : liste de nombre (List[int])


4. Div
   Description : Calcul la division d'un nombre
   Route: '/div/' 
   Accès via : Un token d'authentification
   Paramètres:
   - 'x': Numérateur(integer)
   - item: Modèle Pydantic contenant le diviseur

### Gestion des Utilisateurs
   User
   Description : Obtenir des informations sur l'utilisateur actuel
   Route: '/users/me' 
   Accès via : Un token d'authentification

### Obtention d'un token
   Token
   Description : Obtenir le jeton d'accès
   Route: '/token/' 
   Paramètres:
   - 'username': Nom d'utilisateur 
   - 'password': Mot de passe

### Statistiques
   Stats
   Description : Obtenir le jeton d'accès
   Route: '/stats/' 
   Accès via : Un token d'authentification d'administrateur 


## Compte rendu du projet

Dans FastAPI, les routes doivent être enregistrées auprès de l'instance d'application pour qu'elles soient 
accessibles lorsque le serveur est en cours d'exécution. Dans notre code, les routes sont définies à l'aide de 
décorateurs qui configurent essentiellement le comportement de routage. Cependant, jusqu'à ce qu'on invoque 
les fonctions décorées avec le décorateur @fast_api_decorator, les routes ne sont pas ajoutées à l'application 
FastAPI. En effet, lors du lancement de l'application, le programme app.py est exécuté mais les routes ne sont pas 
ajoutées tant que le décorateur n'est pas appelé, c'est-à-dire que les fonctions décorées ne sont pas exécutées une
première fois. Il est alors nécessaire d'appeler chaque fonction dans le programme app afin de rendre utilisable
leur route.
