import pytest
from corfumv.schemas import ExperimentsEntitry, ModelsEntity


@pytest.mark.usefixtures("init_exp", "init_model")
class TestClientsExperiment:

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
                       init_exp: ExperimentsEntitry,
                       init_model: ModelsEntity):
        resp = init_exp.add_model(model=init_model)
        assert resp == {
            "message": "experiment successfully updated",
            "object_id": init_exp.id,
            "update": "add_model",
            "modefied_count": 1
        }


    def test_remove_model(self,
                          init_exp: ExperimentsEntitry,
                          init_model: ModelsEntity):
        resp = init_exp.remove_model(model=init_model)
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
