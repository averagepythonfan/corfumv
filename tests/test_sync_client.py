import pytest
from corfumv.client import CorfuClient
from corfumv.schemas import ExperimentsEntitry


class TestClient:

    client: CorfuClient = CorfuClient(uri="http://localhost:11000")

    def test_expinstance(self):
        exp: ExperimentsEntitry = self.client.create_experiment(
            name="test_client",
            tags=["test", "dev"]
        )
        assert isinstance(exp, ExperimentsEntitry)
        exp.delete()


    def test_rename_experiment(self):
        exp: ExperimentsEntitry = self.client.create_experiment(
            name="test_client",
            tags=["test", "dev"]
        )
        resp = exp.rename(new_name="renamed")
        assert resp == {
            "message": "experiment successfully updated",
            "object_id": exp.id,
            "update": "rename",
            "modefied_count": 1
        }
        exp.delete()


    # def test_delete_exp(self):
    #     resp = self.exp.delete()
    #     assert resp == {
    #         "message": "experiment deleted",
    #         "object_id": self.exp.id,
    #         "deleted_count": 1
    #     }
