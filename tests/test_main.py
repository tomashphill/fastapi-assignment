import logging

from fastapi import FastAPI
from fastapi.testclient import TestClient # type: ignore

from .json_db import *
from app.dependencies import get_db
from app.routers import tags


app = FastAPI()
app.include_router(tags.router)

mock_db = MockDB()
def get_mock_db() -> DB:
    return mock_db

# override database dependency with mock database
app.dependency_overrides[get_db] = get_mock_db


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
            'ctx': {'pattern': '[a-z_]{3,15}'}, 
            'loc': ['body', 'name'], 
            'msg': 'string does not match regex "[a-z_]{3,15}"', 
            'type': 'value_error.str.regex'
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
            'ctx': {'limit_value': 10}, 
            'loc': ['body', 'value'], 
            'msg': 'ensure this value is less than 10', 
            'type': 'value_error.number.not_lt'
        }]
    }

def test_get_tags():
    response = client.get('/tag')
    assert response.status_code == 200
    assert response.json() == {
        "ballz": 6
    }

