all: build

build:
	@rm -rf dist
	@uv build

format:
	@uv run black .

lint:
	@uv run pylint ./pureskillgg_csgo_dsdk
	@uv run black --check .

test:
	@uv run pytest --cov=./pureskillgg_csgo_dsdk

watch:
	@uv run ptw

version:
	@git add pyproject.toml uv.lock
	@git commit -m "$$(uv version --short)"
	@git tag --sign "v$$(uv version --short)" -m "$(uv version --short)"
	@git push --follow-tags

.PHONY: build format lint test watch version
