# CorfuMV - fast, light and clear framework to versioning your TensorFlow models

## Install now

* `pip install https://github.com/averagepythonfan/corfumv/archive/main.zip`

## What is that all about?

1. We develope machine learning models
2. We need light and fast framework to versioning models
3. We use CorfuMV


## Firstly, we need to up our CorfuMV server and MongoDB
```
# docker-compose.yml
version: "3.3"

services:
  mongodb:
    image: mongo:latest
    container_name: mongodb
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: secret
  corfumv:
    image: zhenyaover9000/corfumv:0.2.2.post0
    container_name: corfumv
    environment:
      MONGO: mongodb://root:secret@mongodb:27017
      SYNC: True
    volumes:
      - "./corfumv:/app/corfumv"
    ports:
      - "11000:11000"
    entrypoint: uvicorn corfumv.server:app --host 0.0.0.0 --port 11000 --reload
```

and then up services:
```
~$: docker compose up -d
```

## Code example:

```Python
>>> from corfumv.client import CorfuClient
>>> client = CorfuClient("http://localhost:11000")
>>> exp = client.create_experiment(name="test_del", tags=["test", "delete"])
>>> exp.id
... '658432fe394f866bc0096605'
>>> md = client.create_model(name="test_md", tags=["test", "model"])
>>> md.id
... '6584339e394f866bc0096607'

```
