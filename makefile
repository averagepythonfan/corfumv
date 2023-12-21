swagger:
	firefox --new-tab http://localhost:11000/docs

lab_url:
	firefox $(shell docker logs lab_corfumv 2>&1 | grep 'http://127.0.0.1:8080/lab?token=' | tail -n 1)

run_tests:
	docker compose -f docker-compose-test.yml up -d
	sleep 1
	poetry run pytest -v
	docker compose -f docker-compose-test.yml down

rebuild:
	rm -f dist/*
	poetry build --format wheel
	docker exec lab_corfumv bash -c 'pip install --force-reinstall /app/dist/*'

ruff:
	poetry run ruff check corfumv/ --fix

image_build:
	poetry run ansible-playbook build.yml
