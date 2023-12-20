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
        del_resp = exp.delete()
        assert del_resp["deleted_count"] == 1


    async def test_find_model(self, async_client):
        md = await async_client.find_model_by(
            find_by="name",
            value="test_async_client_md"
        )
        assert isinstance(md, ModelsEntity)
        assert md.name == "test_async_client_md"
        print(md)
        del_resp = md.delete()
        assert del_resp["deleted_count"] == 1


# import pytest
# from httpx import AsyncClient, Response
# from bson import ObjectId


# async def async_request(method: str,
#                         url: str,
#                         params: dict = None,
#                         json: dict = None) -> Response:
#     async with AsyncClient() as session:
#         return await session.request(
#             method=method,
#             url=url,
#             params=params,
#             json=json
#         )


# exp1, exp2, exp3 = [ObjectId().binary.hex() for _ in range(3)]


# @pytest.mark.parametrize(
#         argnames="hex_id, name, tags",
#         argvalues=[
#             (exp1, "test_exp1", ["test", "raw"]),
#             (exp2, "test_exp2", ["test1", "raw"]),
#             (exp3, "test_exp3", ["test2", "raw"]),
#         ]
# )
# async def test_create_experiment(hex_id, name, tags):
#     options = {
#         "method": "POST",
#         "url": "http://localhost:12000" + "/experiments" + "/create",
#         "json": {
#             "_id": hex_id,
#             "name": name,
#             "tags": tags,
#         }
#     }
#     result = await async_request(**options)
#     assert result.status_code == 200


# @pytest.mark.parametrize(
#         argnames="hex_id",
#         argvalues=[
#             (exp1),
#             (exp2),
#             (exp3),
#         ]
# )
# async def test_delete_experiments(hex_id):
#     options = {
#         "method": "DELETE",
#         "url": "http://localhost:12000" + "/experiments" + "/delete",
#         "params": {
#             "instance_id": hex_id
#         }
#     }
#     result = await async_request(**options)
#     assert result.status_code == 200
