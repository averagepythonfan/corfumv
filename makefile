mongo_up:
	docker run --rm -d -e MONGO_INITDB_ROOT_USERNAME=root -e MONGO_INITDB_ROOT_PASSWORD=secret --name=mongo mongo:latest

mongo_ip:
	echo mongodb://root:secret@$(shell docker inspect -f "{{.NetworkSettings.Networks.bridge.IPAddress}}" mongo):27017

corfumv_rebuild:
	docker compose stop corfumv && docker compose rm corfumv -f && docker compose build corfumv && docker compose up -d

swagger:
	firefox --new-tab http://localhost:11000/docs

lab_url:
	firefox $(shell docker logs lab_corfumv 2>&1 | grep 'http://127.0.0.1:8080/lab?token=' | tail -n 1)

test_mongo_up:
	docker run --rm -d -e MONGO_INITDB_ROOT_USERNAME=test -e MONGO_INITDB_ROOT_PASSWORD=test --name=mongo_test -p 27017:27017 mongo:latest
	sleep 1
	poetry run pytest -v
	docker stop mongo_test

rebuild:
	rm -f dist/*
	poetry build --format wheel
	docker exec lab_corfumv bash -c 'pip install /app/dist/*'
