.PHONY: build

docker-build:
	@docker-compose build

docker-worker:
	@docker-compose run --rm worker

docker-start-tournament:
	@docker-compose run --rm start-tournament

docker-generate-token-pickle:
	@docker-compose run --rm generate-token-pickle

generate-token-pickle:
	pipenv run python src/generate-token-pickle.py

run:
	@pipenv run python src/worker.py

update-wheels:
	pipenv run python setup.py bdist_wheel --universal
	pipenv run pip install --force-reinstall --no-deps --find-links=dist super_draft
