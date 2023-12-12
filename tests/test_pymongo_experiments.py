import datetime
import pytest
from bson import ObjectId
from conftest import pymongo_client_service


client = pymongo_client_service()
item_1, item_2, item_3 = [ObjectId().binary.hex() for _ in range(3)]


@pytest.mark.parametrize(
    argnames="gen_id, name, tags",
    argvalues=[
        (item_1, "first_try", ["v0.1.1", "alpha"]),
        (item_2, "sec_try", ["v0.2.3", "beta", "temporary"]),
        (item_3, "last_try", ["v0.5.2", "rc"]),
    ]
)
def test_create_experiment(gen_id, name, tags):
    response = client.post(
        "/experiments/create",
        json={
            "_id": gen_id,
            "name": name,
            "tags": tags
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "experiment created successfully",
        "object_id": gen_id,
        "name": name
    }


def test_experiment_list():
    response = client.get(
        "/experiments/list",
        params={
            'num': '10',
            'page': '0',
        }   
    )
    assert response.status_code == 200
    assert len(response.json()) == 3


@pytest.mark.parametrize(
    argnames="find_by, value, is_list",
    argvalues=[
        ("name", "sec_try", "false"),
        ("tags", "beta", "false"),
        ("date", str(datetime.datetime.now()), "true"),
    ]
)
def test_find_by(find_by, value, is_list):
    response = client.get(
        "/experiments/find_by",
        params={
            "find_by": find_by,
            "value": value,
            "is_list": is_list,
        }
    )
    assert response.status_code == 200


@pytest.mark.parametrize(
        argnames="instance_id, update, value",
        argvalues=[
            (item_1, "rename", "renamed"),
            (item_1, "add_tag", "added_tag"),
            (item_1, "remove_tag", "added_tag"),
            (item_2, "add_model", "28arg05gj00d2v9j]qj0w"),
            (item_2, "remove_model", "28arg05gj00d2v9j]qj0w"),
        ]
)
def test_update(instance_id, update, value):
    response = client.patch(
        "/experiments/set",
        params={
            'instance_id': instance_id,
            'update': update,
            'value': value,
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "experiment successfully updated",
        "object_id": instance_id,
        "update": update,
        "modefied_count": 1
    }


@pytest.mark.parametrize(
        argnames="instance_id",
        argvalues=[
            (item_1),
            (item_2),
            (item_3),
        ]
)
def test_delete_experiment(instance_id):
    response = client.delete(
        "/experiments/delete",
        params={"instance_id": instance_id}
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "experiment deleted",
        "object_id": instance_id,
        "deleted_count": 1
    }
