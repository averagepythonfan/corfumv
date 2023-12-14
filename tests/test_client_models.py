import pytest
from corfumv.schemas import ModelsEntity


@pytest.mark.usefixtures("init_model")
class TestClientsModel:

    def test_model_init(self, init_model):
        assert isinstance(init_model, ModelsEntity)

    
    def test_model_rename(self, init_model: ModelsEntity):
        resp = init_model.rename(new_name="renamed")
        assert resp == {
            "message": "model successfully updated",
            "object_id": init_model.id,
            "update": "rename",
            "modefied_count": 1
        }


    def test_model_rename_twice(self, init_model: ModelsEntity):
        resp = init_model.rename(new_name="renamed2")
        assert resp == {
            "message": "model successfully updated",
            "object_id": init_model.id,
            "update": "rename",
            "modefied_count": 1
        }


    def test_add_tag(self, init_model: ModelsEntity):
        resp = init_model.add_tag(tag="new_tag")
        assert resp == {
            "message": "model successfully updated",
            "object_id": init_model.id,
            "update": "add_tag",
            "modefied_count": 1
        }


    def test_remove_tag(self, init_model: ModelsEntity):
        resp = init_model.remove_tag(tag="test")
        assert resp == {
            "message": "model successfully updated",
            "object_id": init_model.id,
            "update": "remove_tag",
            "modefied_count": 1
        }


    def test_set_description(self, init_model: ModelsEntity):
        resp = init_model.set_description(description="new_description")
        assert resp == {
            "message": "model successfully updated",
            "object_id": init_model.id,
            "update": "set_description",
            "modefied_count": 1
        }


    def test_set_config(self, init_model: ModelsEntity):
        conf = {"layer": {"name": "first_layer", "req": "l2"}}
        resp = init_model.set_config(config=conf)
        assert resp == {
            "message": "model successfully updated",
            "object_id": init_model.id,
            "update": "set_config",
            "modefied_count": 1
        }


    def test_set_weight(self, init_model: ModelsEntity):
        weights = [{"layer1": [2, 4, 23, 15, 1, 55, 2554, 2]}]
        resp = init_model.set_weights(weights=weights)
        assert resp == {
            "message": "model successfully updated",
            "object_id": init_model.id,
            "update": "set_weights",
            "modefied_count": 1
        }


    def test_delete_exp(self, init_model: ModelsEntity):
        resp = init_model.delete()
        assert resp == {
            "message": "model deleted",
            "object_id": init_model.id,
            "deleted_count": 1
        }
