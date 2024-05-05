# Documentation du Projet DataExoAPI

Ce projet met en œuvre une API FastAPI avec une base de données SQLAlchemy, des migrations gérées par Alembic, et utilise Redis comme système de cache pour améliorer les performances de l'API.

### Environnement Virtuel (DataExo)

Pour développer ce projet, vous devez d'abord configurer un environnement virtuel.

```bash
python -m venv DataExo
```
```bash
source DataExo/bin/activate
```

### Installation des Dépendances

Installez les dépendances du projet à l'aide du fichier requirements.txt.

```bash
pip install -r requirements.txt
```
#### Création de la Base de Données

La base de données mydatabase.db est créée dans le fichier db.py.

Les modèles SQLAlchemy sont définis dans le fichier models.py. La classe User définit la table users avec les colonnes id, username, et email.

### Gestion des Migrations avec Alembic

Configuration d'Alembic : 

* Fichier alembic.ini : Configuration principale d'Alembic, specifier le chemin d'acces vers la bd en remplacant **sqlalchemy.url = sqlite:///mydatabase.db**
* Fichier env.py : Importer Base depuis le fichier models.
 python
```python
from models import Base
target_metadata = Base.metadata
```
* Initialisation des Migrations
```bash
alembic init alembic
```
* Génération d'une Migration
```bash
alembic revision -m "create_users_table"
```
* Application des Migrations
```bash
alembic upgrade head
```
* Validation des Migrations
```bash
alembic history
```
### Lancement de l'application 

**main.py :**  Le fichier main.py définit les routes de l'API FastAPI.
```bash 
uvicorn main:app --reload
```

**UnitTests.py :** Le fichier UnitTests.py contient les tests unitaires pour chaque fonctionnalité de l'API

```bash 
pytest -v UnitTests.py
```

# Utilisation de Docker Compose

Utilisez Docker Compose pour configurer l'environnement de base de données avec le fichier. 

* Configuration du fichier Dockerfile
Le fichier Dockerfile est configuré pour construire l'image Docker de votre application FastAPI. Assurez-vous d'inclure toutes les dépendances nécessaires et de définir la commande de démarrage de votre application.

* Configuration du fichier docker-compose.yml
Le fichier docker-compose.yml est utilisé pour définir les services de votre application, y compris la base de données et potentiellement l'API FastAPI. Configurez ce fichier pour définir les services nécessaires, tels que les volumes, les ports exposés, et les dépendances entre les services.
```bash 
sudo usermod -aG docker <your_username>

sudo chmod 666 /var/run/docker.sock

sudo systemctl restart docker

docker-compose build
```

### Utilisation d'un Cache Redis

Intégrez Redis comme système de cache pour l'API.
* Installer redis :
 ```bash
  sudo apt install redis-server
```
* Démmarer redis 
```bash 
sudo systemctl start redis-server
```
* Test de connexion :
```bash
  redis-cli ping
```
import redis

# Connexion à Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Exemple de mise en cache
r.set('user:1', '{"id": 1, "username": "john_doe", "email": "john@example.com"}')
