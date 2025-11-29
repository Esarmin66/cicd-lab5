from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

# Существующие пользователи
users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]

def test_get_existed_user():
    '''Получение существующего пользователя'''
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]

def test_get_unexisted_user():
    '''Получение несуществующего пользователя'''
    response = client.get("/api/v1/user", params={'email': 'nonexistent@mail.com'})
    assert response.status_code == 404
    assert response.json()['detail'] == "User not found"

def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
    new_user = {
        'name': 'Sergey Sergeev',
        'email': 's.s.sergeev@mail.com'
    }

    response = client.post("/api/v1/user", json=new_user)

    assert response.status_code == 201
    assert isinstance(response.json(), int)

    check_response = client.get("/api/v1/user", params={'email': new_user['email']})
    assert check_response.status_code == 200
    created_user = check_response.json()
    assert created_user['name'] == new_user['name']
    assert created_user['email'] == new_user['email']

def test_create_user_with_invalid_email():
    '''Создание пользователя с почтой, которую использует другой пользователь'''
    duplicate_user = {
        'name': 'Another Ivan',
        'email': users[0]['email']
    }

    response = client.post("/api/v1/user", json=duplicate_user)

    assert response.status_code == 409
    assert response.json()['detail'] == "User with this email already exists"

def test_delete_user():
    '''Удаление пользователя'''
    user_to_delete = {
        'name': 'User To Delete',
        'email': 'to.delete@mail.com'
    }

    create_response = client.post("/api/v1/user", json=user_to_delete)
    assert create_response.status_code == 201

    check_response = client.get("/api/v1/user", params={'email': user_to_delete['email']})
    assert check_response.status_code == 200

    delete_response = client.delete("/api/v1/user", params={'email': user_to_delete['email']})
    assert delete_response.status_code == 204

    final_check = client.get("/api/v1/user", params={'email': user_to_delete['email']})
    assert final_check.status_code == 404
