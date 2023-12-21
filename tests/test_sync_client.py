import pytest
from tests.conftest import TEST_CORFUMV_URI
from corfumv.schemas import ModelsEntity, ModelParams, ExperimentsEntitry
from corfumv.client import CorfuClient


@pytest.fixture(scope="module")
def sync_client():
    sync_client: CorfuClient = CorfuClient(uri=TEST_CORFUMV_URI)
    yield sync_client


@pytest.mark.usefixtures("sync_client")
class TestClient:


    def test_create_exp(self, sync_client):
        md: ModelsEntity = sync_client.create_model(
                name="test_clients_md",
                tags=["test", "dev"],
                params=[ModelParams(parameter="batch", value=120)],
                description="test model"
            )
        assert isinstance(md, ModelsEntity)
    

    def test_create_experiment(self, sync_client):
        exp: ExperimentsEntitry = sync_client.create_experiment(
            name="test_clients_exp",
            tags=["test", "dev"]
        )
        assert isinstance(exp, ExperimentsEntitry)


    def test_list_of_experiment(self, sync_client):
        exp_list = sync_client.list_of_experiments()
        assert len(exp_list) == 1
    

    def test_list_of_models(self, sync_client):
        models_list = sync_client.list_of_models()
        assert len(models_list) == 1
    

    def test_find_experiment(self, sync_client):
        exp = sync_client.find_experiment_by(
            find_by="name",
            value="test_clients_exp"
        )
        assert isinstance(exp, ExperimentsEntitry)
        assert exp.name == "test_clients_exp"
    

    def test_find_model(self, sync_client):
        md = sync_client.find_model_by(
            find_by="name",
            value="test_clients_md"
        )
        assert isinstance(md, ModelsEntity)
        assert md.name == "test_clients_md"
