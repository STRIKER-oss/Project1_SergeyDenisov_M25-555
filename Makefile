install:
	poetry install

project:
	poetry run project

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install  dist/*.whl

lint:
	poetry run ruff check .

clean:
	rm -rf dist
	rm -rf .ruff_cache
