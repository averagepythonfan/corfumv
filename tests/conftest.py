import pytest
from fastapi.testclient import TestClient
from pymongo import MongoClient
from corfumv.server import app
from corfumv.client import CorfuClient
from corfumv.mongo import get_service, PymongoUnitOfWork, PymongoCRUDService
from corfumv.schemas import ExperimentsEntitry, ModelParams, ModelsEntity


TEST_CORFUMV_URI = "http://localhost:12000"
TEST_MONGO_URI = "mongodb://test:test@localhost:27017"


@pytest.fixture(scope="module")
def test_client():
    test_mongo = MongoClient(TEST_MONGO_URI)

    def override_get_service():
        return PymongoCRUDService(uow=PymongoUnitOfWork(client=test_mongo))

    app.dependency_overrides[get_service] = override_get_service
    yield TestClient(app=app)


@pytest.fixture(scope="module")
def init_model():
    client: CorfuClient = CorfuClient(uri=TEST_CORFUMV_URI)
    md: ModelsEntity = client.create_model(
                name="test_model",
                tags=["test", "dev"],
                params=[ModelParams(parameter="batch", value=120)],
                description="test model"
            )
    yield md
    md.delete()


@pytest.fixture(scope="module")
def init_exp():
    client: CorfuClient = CorfuClient(uri=TEST_CORFUMV_URI)
    exp: ExperimentsEntitry = client.create_experiment(
            name="test_exp",
            tags=["test", "dev"]
        )
    yield exp
    exp.delete()
