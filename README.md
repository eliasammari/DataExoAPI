# Documentation du Projet DataExoAPI

Ce projet met en œuvre une API FastAPI avec une base de données SQLAlchemy, des migrations gérées par Alembic, et utilise Redis comme système de cache pour améliorer les performances de l'API.

### Environnement Virtuel (DataExo)

Pour développer ce projet, vous devez d'abord configurer un environnement virtuel.

```bash
python -m venv DataExo
```
source DataExo/bin/activate

### Installation des Dépendances

Installez les dépendances du projet à l'aide du fichier requirements.txt.

*  pip install -r requirements.txt

#### Création de la Base de Données

La base de données mydatabase.db est créée dans le fichier db.py.

Modèles SQLAlchemy (models.py)

Les modèles SQLAlchemy sont définis dans le fichier models.py. La classe User définit la table users avec les colonnes id, username, et email.

### Gestion des Migrations avec Alembic

Configuration d'Alembic : 

Fichier alembic.ini : Configuration principale d'Alembic, specifier le chemin d'acces vers la bd en remplacant 
Fichier env.py : Importer Base depuis le fichier models.

* Initialisation des Migrations
Commande Bash : alembic init alembic

* Génération d'une Migration
Commande Bash : alembic revision -m "create_users_table"

* Application des Migrations
Commande Bash : alembic upgrade head

* Validation des Migrations
Commande Bash : alembic history

### Lancement de l'application 

**main.py :**  Le fichier main.py définit les routes de l'API FastAPI.
*
*

**UnitTests.py :** Le fichier UnitTests.py contient les tests unitaires pour chaque fonctionnalité de l'API
*
*

### Utilisation de Docker Compose

Utilisez Docker Compose pour configurer l'environnement de base de données avec le fichier. 

Configurer le fichier dockerfile pour 
Configurer le fichier docker-compose.yml pour : 

### Utilisation d'un Cache Redis

Intégrez Redis comme système de cache pour l'API.

import redis

# Connexion à Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Exemple de mise en cache
r.set('user:1', '{"id": 1, "username": "john_doe", "email": "john@example.com"}')
