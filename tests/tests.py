import pytest

from src.app import app, db, UserModel


@pytest.fixture()
def get_client():
    yield app.test_client()


def test_database(get_client):
    assert get_client.get('/').status_code == 200


def test_add_user(get_client):
    assert get_client.post('/add/user').status_code == 400


def test_start_streaming_first(get_client):
    assert get_client.post('/start').status_code == 400


def test_start_streaming_second(get_client):
    assert get_client.post("/start", data={
        'camera_ip' : "0.0.0.0",
    }).status_code == 302


def test_user_view(get_client):
    user = UserModel("123456789a")
    db.session.add(user)
    db.session.commit()

    assert b"123456789a" in get_client.get("/users").data

    user = db.session.query(UserModel).filter(UserModel.name == "123456789a").first()
    db.session.delete(user)
    db.session.commit()



