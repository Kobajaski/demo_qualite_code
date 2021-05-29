.PHONY: install
install:
	@pip install -e .
	@pipenv install $(OPTIONS)

.PHONY: build
build:
	@python setup.py sdist bdist_wheel

.PHONY: run
run:
	@tutoapi $(OPTIONS)

.PHONY: tox
tox:
	@tox $(OPTIONS)

.PHONY: test
test:
	@tox -e pytest

.PHONY: lint
lint:
	@tox -e isort
	@tox -e black
	@tox -e flake8
	@tox -e mypy

.PHONY: security
security:
	@tox -e bandit
	@tox -e safety

.PHONY: docs
docs:
	@tox -e apidocs
	@tox -e docs

.PHONY: clean
clean:
	@find . -type f -name '*.pyc' -delete
	@find . -type d -name '__pycache__' | xargs rm -rf
	@rm -rf build/
	@rm -rf dist/
	@rm -rf *.egg*
	@rm -rf docs/build/
	@rm -f .coverage*
	@rm -rf .tox
	@rm -rf .mypy_cache
