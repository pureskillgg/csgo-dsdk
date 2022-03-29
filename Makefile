all: lint test

build:
	@rm -rf dist
	@poetry build

format:
	@poetry run black .

lint:
	@poetry run pylint ./pureskillgg_csgo_dsdk
	@poetry run black --check .

publish:
	@poetry run twine upload --skip-existing dist/*

test:
	@poetry run pytest --cov=./pureskillgg_csgo_dsdk

watch:
	@poetry run ptw

.PHONY: build docs test
