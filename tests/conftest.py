import pytest
from fastapi.testclient import TestClient
from pymongo import MongoClient
from corfumv import app
from corfumv.client import CorfuClient
from corfumv.mongo import get_service, PymongoUnitOfWork, PymongoCRUDService
from corfumv.schemas import ExperimentsEntitry, ModelParams, ModelsEntity


def test_client():
    TEST_MONGO_URI = "mongodb://test:test@localhost:27017"
    test_mongo = MongoClient(TEST_MONGO_URI)

    def override_get_service():
        return PymongoCRUDService(uow=PymongoUnitOfWork(client=test_mongo))

    app.dependency_overrides[get_service] = override_get_service
    return TestClient(app=app)


TEST_CORFUMV_URI = "http://localhost:12000"
client: CorfuClient = CorfuClient(uri=TEST_CORFUMV_URI)


@pytest.fixture(scope="session")
def init_model():
    md: ModelsEntity = client.create_model(
                name="test_model",
                tags=["test", "dev"],
                params=[ModelParams(parameter="batch", value=120)],
                description="test model"
            )
    yield md
    md.delete()


@pytest.fixture(scope="session")
def init_exp():
    exp: ExperimentsEntitry = client.create_experiment(
            name="test_exp",
            tags=["test", "dev"]
        )
    yield exp
    exp.delete()
