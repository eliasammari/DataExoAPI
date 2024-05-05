import pytest
from fastapi.testclient import TestClient
from main import app  
from db import get_session
import asyncio
import aiohttp
import warnings


warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)


client = TestClient(app)

    
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_create_user():
    user_data = {"username": "unexemple","email": "unexemple@gmail.com"}

    response = client.post("/users/", json=user_data)

    assert response.status_code == 200

    data = response.json()
    assert "username" in data
    assert "email" in data
    assert "id" in data

    # Vérifie que les valeurs correspondent aux données envoyées
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]

def test_create_and_delete_user():
    # Créer un nouvel utilisateur
    user_data = {"username": "dindon", "email": "dindon@gmail.com"}
    response = client.post("/users/", json=user_data)

    # Vérifier que la création de l'utilisateur a réussi
    assert response.status_code == 200
    data = response.json()
    assert "username" in data
    assert "email" in data
    assert "id" in data

    user_id = data["id"]

    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]

    # Supprimer l'utilisateur créé
    delete_response = client.delete(f"/users/{user_id}")
    assert delete_response.status_code == 200
    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 404 


def test_update_user_with_specific_id():
    user_id = 1

    updated_data = {"username": "updated_username", "email": "updated_email@example.com"}
    update_response = client.put(f"/users/{user_id}", json=updated_data)
    assert update_response.status_code == 200
    get_response = client.get(f"/users/{user_id}")

    assert get_response.status_code == 200
    updated_user = get_response.json()
    assert updated_user["id"] == user_id
    assert updated_user["username"] == updated_data["username"]
    assert updated_user["email"] == updated_data["email"]