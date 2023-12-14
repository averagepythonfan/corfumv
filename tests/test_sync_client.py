import pytest
from conftest import client
from corfumv.schemas import ModelsEntity, ModelParams, ExperimentsEntitry


class TestClient:


    def test_create_exp(self):
        md: ModelsEntity = client.create_model(
                name="test_clients_md",
                tags=["test", "dev"],
                params=[ModelParams(parameter="batch", value=120)],
                description="test model"
            )
        assert isinstance(md, ModelsEntity)
    

    def test_create_experiment(self):
        exp: ExperimentsEntitry = client.create_experiment(
            name="test_clients_exp",
            tags=["test", "dev"]
        )
        assert isinstance(exp, ExperimentsEntitry)


    def test_list_of_experiment(self):
        exp_list = client.list_of_experiments()
        assert len(exp_list) == 1
    

    def test_list_of_models(self):
        models_list = client.list_of_models()
        assert len(models_list) == 1
    

    def test_find_experiment(self):
        exp = client.find_experiment_by(
            find_by="name",
            value="test_clients_exp"
        )
        assert isinstance(exp, ExperimentsEntitry)
        assert exp.name == "test_clients_exp"
    

    def test_find_model(self):
        md = client.find_model_by(
            find_by="name",
            value="test_clients_md"
        )
        assert isinstance(md, ModelsEntity)
        assert md.name == "test_clients_md"
