from numpy import array
import pytest
from corfumv.schemas import ModelsEntity, ModelParams, ModelMetrics


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


    def test_add_params_by_str(self, init_model: ModelsEntity):
        resp = init_model.add_param(
            parameter="batch_size",
            value=120
        )
        assert resp == {
            "message": "model successfully updated",
            "object_id": init_model.id,
            "update": "add_params",
            "modefied_count": 1
        }


    def test_add_params_by_MP(self, init_model: ModelsEntity):
        p = ModelParams(parameter="seed", value=801)
        resp = init_model.add_param(parameter=p)
        assert resp == {
            "message": "model successfully updated",
            "object_id": init_model.id,
            "update": "add_params",
            "modefied_count": 1
        }


    def test_add_metric_by_str(self, init_model: ModelsEntity):
        resp = init_model.add_metric(
            metric="accuracy",
            value=0.80
        )
        assert resp == {
            "message": "model successfully updated",
            "object_id": init_model.id,
            "update": "add_metric",
            "modefied_count": 1
        }


    def test_add_metric_by_MM(self, init_model: ModelsEntity):
        m = ModelMetrics(metric="f1-score", value=0.68)
        resp = init_model.add_metric(metric=m)
        assert resp == {
            "message": "model successfully updated",
            "object_id": init_model.id,
            "update": "add_metric",
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
        weights = [
            array([2, 4, 23, 15, 1, 55, 2554, 2]),
            array([6, 3, 3, 15, 12, 5, 4, 27]),
        ]
        resp = init_model.set_weights(weights=weights)
        assert resp == {
            "message": "model successfully updated",
            "object_id": init_model.id,
            "update": "set_weights",
            "modefied_count": 1
        }


    def test_delete_params(self, init_model: ModelsEntity):
        resp = init_model.remove_params(param_name="batch_size")
        assert resp == {
            "message": "model successfully updated",
            "object_id": init_model.id,
            "update": "remove_params",
            "modefied_count": 1
        }


    def test_delete_metrics(self, init_model: ModelsEntity):
        resp = init_model.remove_metric(metric_name="f1-score")
        assert resp == {
            "message": "model successfully updated",
            "object_id": init_model.id,
            "update": "remove_metric",
            "modefied_count": 1
        }

