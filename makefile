mongo_up:
	docker run --rm -d -e MONGO_INITDB_ROOT_USERNAME=root -e MONGO_INITDB_ROOT_PASSWORD=secret --name=mongo mongo:latest

mongo_ip:
	echo mongodb://root:secret@$(shell docker inspect -f "{{.NetworkSettings.Networks.bridge.IPAddress}}" mongo):27017

corfumv_rebuild:
	docker compose stop corfumv && docker compose rm corfumv -f && docker compose build corfumv && docker compose up -d

swagger:
	firefox --new-tab http://localhost:11000/docs

test_mongo_up:
	docker run --rm -d -e MONGO_INITDB_ROOT_USERNAME=test -e MONGO_INITDB_ROOT_PASSWORD=test --name=mongo_test -p 27017:27017 mongo:latest
	sleep 2
	pytest -v
	docker stop mongo_test
