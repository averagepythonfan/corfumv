import datetime
import pytest
from bson import ObjectId


item_1, item_2, item_3 = [ObjectId().binary.hex() for _ in range(3)]


@pytest.mark.usefixtures("test_client")
class TestExperiments:

    @pytest.mark.parametrize(
        argnames="gen_id, name, tags",
        argvalues=[
            (item_1, "first_try", ["v0.1.1", "alpha"]),
            (item_2, "sec_try", ["v0.2.3", "beta", "temporary"]),
            (item_3, "last_try", ["v0.5.2", "rc"]),
        ]
    )
    def test_create_experiment(self, gen_id, name, tags, test_client):
        response = test_client.post(
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


    def test_experiment_list(self, test_client):
        response = test_client.get(
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
    def test_find_by(self, find_by, value, is_list, test_client):
        response = test_client.get(
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
            ]
    )
    def test_update(self, instance_id, update, value, test_client):
        response = test_client.patch(
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


    def test_add_model(self, test_client):
        response = test_client.patch(
            "/experiments/set",
            params={
                'instance_id': item_2,
                'update': "add_model",
                'value': "23840hvf98hv9vqh98vr",
            }
        )
        assert response.status_code == 435


    @pytest.mark.parametrize(
            argnames="instance_id",
            argvalues=[
                (item_1),
                (item_2),
                (item_3),
            ]
    )
    def test_delete_experiment(self, instance_id, test_client):
        response = test_client.delete(
            "/experiments/delete",
            params={"instance_id": instance_id}
        )
        assert response.status_code == 200
        assert response.json() == {
            "message": "experiment deleted",
            "object_id": instance_id,
            "deleted_count": 1
        }
