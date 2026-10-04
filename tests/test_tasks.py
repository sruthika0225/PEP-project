import pytest
from app import app
from database.db import init_db

@pytest.fixture
def client(tmp_path, monkeypatch):
    import config

    db_path = tmp_path / "test.db"
    monkeypatch.setattr(config.Config, "DATABASE_PATH", db_path)
    init_db()

    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Task Alarm" in response.data

def test_add_task(client):
    response = client.post("/add-task", data={
        "title": "Test Task",
        "description": "Test description",
        "alarm_date": "2030-01-01",
        "alarm_time": "10:00",
        "repeat": "once"
    })

    assert response.status_code == 302

    response = client.get("/")
    assert b"Test Task" in response.data

def test_delete_task(client):
    client.post("/add-task", data={
        "title": "Delete Me",
        "description": "",
        "alarm_date": "2030-01-01",
        "alarm_time": "10:00",
        "repeat": "once"
    })

    from database import db
    task = db.get_tasks()[0]

    response = client.post(f"/delete-task/{task['id']}")
    assert response.status_code == 302

    assert db.get_task(task["id"]) is None
