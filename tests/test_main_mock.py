from fastapi.testclient import TestClient # type: ignore
from pytest_mock import MockerFixture

from app.main import app
from app.model.database.db import *


client = TestClient(app)


def test_get_all_tags_method_empty_db(mocker: MockerFixture):
    mocker.patch(
        "app.model.database.firestore.FireStore.get_all_tags",
        return_value=[]
    )

    response = client.get("/tag")

    assert response.status_code == 200
    assert response.json() == {}


def test_get_tags(mocker: MockerFixture):
    mocker.patch(
        "app.model.database.firestore.FireStore.get_all_tags",
        return_value=[Tag.parse_obj({"name": "ballz", "value": 6})]
    )

    response = client.get('/tag')

    assert response.status_code == 200
    assert response.json() == {
        "ballz": 6
    }


def test_increment_tag(mocker: MockerFixture):
    mocker.patch(
        "app.model.database.firestore.FireStore.increment_tag",
        return_value=Tag.parse_obj({"name": "ballz", "value": 4})
    )

    response = client.post(
        "/tag",
        json={"name": "ballz", "value": 4}
    )

    assert response.status_code == 200
    assert response.json() == {"name": "ballz", "value": 4}


def test_increment_existing_tag(mocker: MockerFixture):
    mocker.patch(
        "app.model.database.firestore.FireStore.increment_tag",
        return_value=Tag.parse_obj({"name": "ballz", "value": 6})
    )

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


