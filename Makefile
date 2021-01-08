all: lint test

build:
	@rm -rf dist
	@poetry build

clean:
	@rm -rf .pytest-incremental

format:
	@poetry run black .

lint:
	@poetry run pylint ./pureskillgg_makenew_pypackage
	@poetry run black --check .

publish:
	@poetry run twine upload --skip-existing --repository-url https://pureskillgg.jfrog.io/artifactory/api/pypi/pureskillgg-makenew-pypackage dist/*

test:
	@poetry run pytest --inc --cov=./pureskillgg_makenew_pypackage

watch:
	@poetry run ptw

.PHONY: build docs test
