# FastApi Decorator Builder

"FastApi Decorator Builder" est un algorithme permettant de concevoir un décorateur Python qui transforme 
une fonction Python en une API FastAPI. Cette API est rendu flexible par de nombreux arguments de configuration
telle que la route, la méthode, les types d'arguments de la fonction et l'authentification de l'utilisateur pour 
accéder à la réponse de l'API. L'application FastAPI permet également de collecter des données statistiques sur les 
requêtes des différentes routes, leur temps moyen d'exécution ainsi que le nombre d'appels à chaque fonction 
décorée du décorateur @fast_api_decorator. Enfin, notre application est dotée d'un accès à des variables 
d'environnement dans les fonctions à partir d'un fichier de configuration et possède un système de limitation 
du nombre de requêtes autorisées sur une période donnée pour prévenir la surcharge du serveur.

## Installation

1. Télécharger les fichiers Python
2. Installer l'application FastAPI et des packages utilitaires 
```python
$ pip install fastapi
$ pip install python-multipart
$ pip install pydantic
$ pip install pydantic-settings
$ pip install --upgrade packaging
```
3. Installer le serveur ASGI
```python
$ pip install "uvicorn[standard]"
```
4. Lancer le serveur dans le terminal de l'application Python 
```python
$ python -m uvicorn main:app --reload
```
5. Le serveur API démarrera et sera accessible à l'adresse suivante : 
```python
http://127.0.0.1:8000
```
6. Un aperçu des requêtes implémentées est disponible à l'adresse suivante : 
```python
http://127.0.0.1:8000/docs
```


## Utilisation
1. Le décorateur

Le décorateur '@fast_api_decorator' ajoute une route avec un endpoint correspondant aux paramètres de la requête 
(paramètres de la fonction). Le décorateur appliqué à une fonction puis exécutée sur le même script de l'instance 
FastAPI "app" permet de rendre utilisable l'API avec une route qui dépend de la fonction et de ses propres paramètres. 
Ainsi, une fois cette étape réalisée, il est possible de requêter l'API de la fonction à laquelle on a appliqué le
décorateur avec n'importe quels arguments. La réponse de l'API est évidemment l'output de cette fonction. 
L'API est configurée directement grâce aux paramètres du décorateur avec les routes (ex: "/power/", "/add/" ou "/sous/"), les méthodes HTTP (ex: "GET", "POST", "PUT", "DELETE") et une liste de types correspondant aux types des arguments de la fonction décorée. Prenons l'exemple d'une fonction très simple que nous avons implémenté : la fonction power qui renvoie pour deux nombres de type integer, le premier nombre exposant le second.
L'objectif donc du décorateur est de rendre accessible une API avec une route unique à cette fonction tous les calculs de puissance possible. Pour ce faire, il suffit d'appliquer le décorateur développé avec une route qui est libre, une certaine méthode HTTP, le type des arguments attendus de la fonction et enfin le type d'authentification des utilisateurs.
Cela donne ce qui suit :
```python
@fast_api_decorator(route="/power/", method=["GET"], type_args=[int, int])
def power_function(x: int, a: int, current_user: User = Depends(get_current_active_user)):
    return {f"{x} to the power of {a}": x ** a}
```
Dans cet exemple, le décorateur crée une nouvelle API du type "GET" requêtable à l'adresse http://127.0.0.1:8000/power/ avec 2 arguments de type integer x et a que l'on peut spécifier grâce à l'ajout de "?x=9&a=2" à la fin de l'URL permettant de récupérer le résultat {9 to the power of 2: 81}. Cette fonction "power_function" est donc utilisable sous la forme d'une fonction normale ainsi que sous la forme d'une API "GET" classique.
Pour finir on note ici que l'API, une fois générée, n'est requêtable uniquement sous condition de s'être authentifié
avec un utilisateur "actif".

2. L'authentification

Cette API utilise une authentification OAuth2 Password Bearer pour assurer la sécurité des endpoints. Trois types d'utilisateurs sont définis: administrateur (username : "admin" & password : "secret"), utilisateur régulier 
(username : "bod" & password : "secret1") et utilisateur inactif (username : "alice" & password : "secret2"). 
L'administrateur a accès à toutes les fonctionnalités proposées par l'API dont les statistiques. 
L'utilisateur actif peut utiliser les fonctions mathématiques alors que l'utilisateur inactif ne peut qu'accéder qu'à la fonctionnalité 'info' de l'API. 
Si un token invalide ou si une fonctionnalité réservée à un type d'utilisateur spécifique est renseigné 
sans les permissions nécessaires, l'API renverra une erreur : 
   - 401 Unauthorized: Le token fourni est invalide.
   - 400 Bad Request: Vous n'avez pas les permissions nécessaires pour accéder à cette fonctionnalité.

3. Intégration des variables d'environnement

Des variables d'environnement permettent la configuration de notre API. Grâce au fichier .env, on peut personnaliser les 
paramètres de l'application FastAPI sans avoir à modifier directement le code source. Cela simplifie le déploiement
sur différents environnements et une gestion centralisée de la configuration. L'utilisation de pydantic_settings 
permet de charger ('SettingsConfigDict'), valider (BaseSettings) et utiliser les configurations dans l'API. 

4. Flexibilité des arguments

Les fonctions que le décorateur transforme en API peuvent prendre en entrée n'importe quel type d'argument, autant des types simples comme les string, integer, float que les plus complexes comme les listes, dictionnaire et instance de classe. Les objets complexes nécessitent un traitement particulier lors d'une requête à l'API, le plus souvent comme l'insertion d'un json au sein de la requête. Cette méthode est testable notamment avec notre fonction div qui prend en entrée un objet json contenant un integer. Autre exemple plus simple, les listes, qui elles sont requêtables en ajoutant dans l'URL autant de fois "lst=" si l'argument liste s'appelle "lst" qu'elle ne possède d'objet. 
Exemple lst=[1, 2, 3, 4] --> "route_api_fonction/?lst=1&lst=2&lst=3&lst=4".
Enfin, les arguments des fonctions décorées par notre décorateur font l'objet d'un contrôle lors de l'exécution du 
wrapper afin de vérifier leur cohérence avec les attentes du créateur de la fonction.

5. Suivi des Statistiques

Nous avons mis en place un suivi des statistiques du server lors de son utilisation. Par souci de pertinence des
données, ces informations sont remises à 0 à chaque arrêt du programme. Les informations telles que le nombre d'appels d'API par route, le temps moyen d'exécution des requêtes ainsi que le nombre d'exécutions des fonctions décorées par le décorateur sont collectées et accessibles à l'API "/stats". Le principe de fonctionnement est relativement simple, un fichier pickle est créé lors du lancement du serveur où on stocke un json avec les différents compteurs de nombre de requêtes ou de temps d'exécution. Une API "GET" est en charge d'ouvrir et de lire les données de ce fichier qui sont donc actualisées en temps réel. Enfin, le fichier est détruit lors de l'arrêt du serveur.

6. Système de rate limiting

La fonction rate_limit_middleware agit comme un middleware. Elle prend deux paramètres : request qui représente la 
requête HTTP entrante et call_next qui est une fonction représentant le prochain middleware ou le gestionnaire de route
réel dans le pipeline de traitement. Cela nous permet de traiter les requêtes et en l'ocurrence de les limiter afin 
de ne pas surcharger le server. Nous avons limimé les requêtes à 2 par opérations mathématique en 3 secondes, ceci est 
évidement modulable.


## Fonctionnalités
Dans le code suivant, il y a plusieurs fonctions qui ont été implémenté dans l'API. Certaines fonctions nécessitent 
des authentifications.

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


## Note supplémentaire

Dans FastAPI, les routes doivent être enregistrées auprès de l'instance d'application pour qu'elles soient 
accessibles lorsque le serveur est en cours d'exécution. Dans notre code, les routes sont définies à l'aide de 
décorateurs qui configurent essentiellement le comportement de routage. Cependant, jusqu'à ce qu'on invoque 
les fonctions décorées avec le décorateur @fast_api_decorator, les routes ne sont pas ajoutées à l'application 
FastAPI. En effet, lors du lancement de l'application, le programme app.py est exécuté mais les routes ne sont pas 
ajoutées tant que le décorateur n'est pas appelé, c'est-à-dire que les fonctions décorées ne sont pas exécutées une
première fois. Il est alors nécessaire d'appeler chaque fonction dans le programme app afin de rendre utilisable
leur route. Ceci a été un point important de réflexion lors de la réalisation de notre projet afin de comprendre en
détail le fonctionnement d'une API telle q'implémentée.
