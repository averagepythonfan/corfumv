import datetime
import pytest
from bson import ObjectId
from conftest import pymongo_client_service


client = pymongo_client_service()
item_1, item_2, item_3 = [ObjectId().binary.hex() for _ in range(3)]


@pytest.mark.parametrize(
    argnames="gen_id, name, params, tags, metrics, description",
    argvalues=[
        (
            item_1,
            "model_first",
            [{"parameter": "batch_size","value": 50}],
            ["v.0.1.2-alpha"],
            [{"metric": "f1-score", "value": 0.68}],
            "Test model number 1"
        ),
        (
            item_2,
            "model_second",
            [{"parameter": "batch_size","value": 120}],
            ["v.0.1.2-beta"],
            [{"metric": "f1-score", "value": 0.52}],
            "Test model number 2"
        ),
        (
            item_3,
            "model_third",
            [{"parameter": "batch_size","value": 100}],
            ["v.0.1.3-beta"],
            [{"metric": "f1-score","value": 0.72}, {"metric": "accuracy","value": 0.80}],
            "Test model number 3"
        ),
    ]
)
def test_create_models(gen_id, name, params, tags, metrics, description):
    response = client.post(
        "/models/create",
        json={
            "_id": gen_id,
            "name": name,
            "params": params,
            "tags": tags,
            "metrics": metrics,
            "description": description
        }
    )
    assert response.status_code == 200


@pytest.mark.parametrize(
    argnames="find_by, value, is_list",
    argvalues=[
        ("name", "model_first", "false"),
        ("tags", "v.0.1.3-beta", "false"),
        ("date", str(datetime.datetime.now()), "true"),
    ]
)
def test_find_models_by(find_by, value, is_list):
    response = client.get(
        "/models/find_by",
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
            (item_2, "set_description", "This is parametrize desc"),
            (item_3, "set_description", "This is parametrize desc2"),
        ]
)
def test_update_models(instance_id, update, value):
    response = client.patch(
        "/models/set",
        params={
            'instance_id': instance_id,
            'update': update,
            'value': value,
        }
    )
    assert response.status_code == 200



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
        "/models/delete",
        params={"instance_id": instance_id}
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "model deleted",
        "object_id": instance_id,
        "deleted_count": 1
    }
