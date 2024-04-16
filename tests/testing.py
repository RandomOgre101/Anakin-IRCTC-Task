from app.schemas import schemas
from .test_database import client



def test_root(client):
    res = client.get("/")
    assert res.json().get('message') == "Hello World"
    assert res.status_code == 200


def test_create_admin(client):
    res = client.post("/api/v1/users/", json={'email': 'admin@gmail.com', 'password': 'adminpassword', 'role': 'admin'})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == 'admin@gmail.com'
    assert new_user.id == 1
    assert res.status_code == 201


def test_create_user(client):
    res = client.post(
        "/api/v1/users/", 
        json={'email': 'test@gmail.com', 'password': 'testpassword'}
        )
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == 'test@gmail.com'
    assert new_user.id == 2
    assert res.status_code == 201


def test_login_admin(client):
    res = client.post(
        "api/v1/login/",
        data={'username': 'admin@gmail.com', 'password': 'adminpassword'}
    )
    assert res.status_code == 200


def test_login_user(client):
    res = client.post(
        "api/v1/login/",
        data={'username': 'test@gmail.com', 'password': 'testpassword'}
    )
    assert res.status_code == 200


def test_user_doesnt_exist(client):
    res = client.post(
        "api/v1/login/",
        data={'username': 'notInDB@gmail.com', 'password': 'notInDB'}
    )
    assert res.status_code == 403


def test_get_seat_availability_not_exist(client):
    res = client.post(
        "/api/v1/user/booking/train",
        json={'start': 'Test 1', 'end': 'Test 2'}
    )
    assert res.status_code == 404


