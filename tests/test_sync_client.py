import pytest
from corfumv.client import CorfuClient
from corfumv.schemas import ExperimentsEntitry, ModelParams, ModelsEntity


client: CorfuClient = CorfuClient(uri="http://localhost:11000")
md: ExperimentsEntitry = client.create_model(
            name="test_client",
            tags=["test", "dev"],
            params=[ModelParams(parameter="batch", value=120)],
            description="test model"
        )


@pytest.fixture(scope="session")
def init_exp():
    exp: ExperimentsEntitry = client.create_experiment(
            name="test_client",
            tags=["test", "dev"]
        )
    yield exp
    exp.delete()


class TestClient:

    def test_expinstance(self, init_exp):
        assert isinstance(init_exp, ExperimentsEntitry)


    def test_rename_experiment(self, init_exp):
        resp = init_exp.rename(new_name="renamed")
        assert resp == {
            "message": "experiment successfully updated",
            "object_id": init_exp.id,
            "update": "rename",
            "modefied_count": 1
        }


    def test_rename_experiment_twice(self, init_exp: ExperimentsEntitry):
        resp = init_exp.rename(new_name="renamed2")
        assert resp == {
            "message": "experiment successfully updated",
            "object_id": init_exp.id,
            "update": "rename",
            "modefied_count": 1
        }


    def test_add_tag(self, init_exp: ExperimentsEntitry):
        resp = init_exp.add_tag(tag="new_tag")
        assert resp == {
            "message": "experiment successfully updated",
            "object_id": init_exp.id,
            "update": "add_tag",
            "modefied_count": 1
        }


    def test_remove_tag(self, init_exp: ExperimentsEntitry):
        resp = init_exp.remove_tag(tag="test")
        assert resp == {
            "message": "experiment successfully updated",
            "object_id": init_exp.id,
            "update": "remove_tag",
            "modefied_count": 1
        }


    def test_add_model(self,
                       init_exp: ExperimentsEntitry):
        resp = init_exp.add_model(model=md)
        assert resp == {
            "message": "experiment successfully updated",
            "object_id": init_exp.id,
            "update": "add_model",
            "modefied_count": 1
        }


    def test_remove_model(self,
                          init_exp: ExperimentsEntitry):
        resp = init_exp.remove_model(model=md)
        assert resp == {
            "message": "experiment successfully updated",
            "object_id": init_exp.id,
            "update": "remove_model",
            "modefied_count": 1
        }


    def test_delete_exp(self, init_exp: ExperimentsEntitry):
        resp = init_exp.delete()
        assert resp == {
            "message": "experiment deleted",
            "object_id": init_exp.id,
            "deleted_count": 1
        }
