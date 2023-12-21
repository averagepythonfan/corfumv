import pytest
from tests.conftest import TEST_CORFUMV_URI
from corfumv.client import CorfuAsyncClient
from corfumv.schemas import ModelsEntity, ModelParams, ExperimentsEntitry


@pytest.fixture(scope="module")
def async_client():
    cl = CorfuAsyncClient(uri=TEST_CORFUMV_URI)
    yield cl


@pytest.mark.usefixtures("async_client")
class TestAsyncClient:

    async def test_create_model(self, async_client):
        md: ModelsEntity = await async_client.create_model(
                name="test_async_client_md",
                tags=["test", "dev"],
                params=[ModelParams(parameter="batch", value=120)],
                description="test model"
            )
        assert isinstance(md, ModelsEntity)
    

    async def test_create_experiment(self, async_client):
        exp: ExperimentsEntitry = await async_client.create_experiment(
            name="test_async_clients_exp",
            tags=["test", "dev"]
        )
        assert isinstance(exp, ExperimentsEntitry)


    async def test_list_of_experiment(self, async_client):
        exp_list = await async_client.list_of_experiments()
        assert len(exp_list) == 1
    

    async def test_list_of_models(self, async_client):
        models_list = await async_client.list_of_models()
        assert len(models_list) == 1
    

    async def test_find_experiment(self, async_client):
        exp = await async_client.find_experiment_by(
            find_by="name",
            value="test_async_clients_exp"
        )
        assert isinstance(exp, ExperimentsEntitry)
        assert exp.name == "test_async_clients_exp"
        exp.delete()


    async def test_find_model(self, async_client):
        md = await async_client.find_model_by(
            find_by="name",
            value="test_async_client_md"
        )
        assert isinstance(md, ModelsEntity)
        assert md.name == "test_async_client_md"
        md.delete()