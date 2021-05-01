from fastapi.testclient import TestClient # type: ignore

from app.application import create_app
from .mock_db import *


app = create_app(title="Tagger Tester", db=MockDB())

client = TestClient(app)


def test_get_tag_empty_db():
    response = client.get("/tag")
    assert response.status_code == 200
    assert response.json() == {}

def test_increment_tag():
    response = client.post(
        "/tag",
        json={"name": "ballz", "value": 4}
    )
    assert response.status_code == 200
    assert response.json() == {"name": "ballz", "value": 4}

def test_increment_existing_tag():
    response = client.post(
        "/tag",
        json={"name": "ballz", "value": 2}
    )
    assert response.status_code == 200
    assert response.json() == {"name": "ballz", "value": 6}

def test_increment_tag_invalid_name():
    response = client.post(
        "/tag",
        json={"name": "9lives", "value": 2}
    )
    assert response.status_code == 422
    assert response.json() == {
        'detail': [{
            'loc': ['body', 'name'],
            'msg': '9lives is not a valid string',
            'type': 'value_error'
        }]
    }

def test_increment_tag_invalid_value():
    response = client.post(
        "/tag",
        json={"name": "ballz", "value": 12}
    )
    assert response.status_code == 422
    assert response.json() == {
        'detail': [{
            'loc': ['body', 'value'], 
            'msg': 'value must be a positive integer less than 10', 
            'type': 'value_error'}]
    }

def test_get_tags():
    response = client.get('/tag')
    assert response.status_code == 200
    assert response.json() == {
        "ballz": 6
    }

