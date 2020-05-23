clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

lint: ## check style
	flake8 curlify.py curlify_test.py

test:
	py.test --cov=curlify --cov-report term-missing --cov-fail-under=95 --cov-branch

test-all: lint test

install:
	pip install . --upgrade

install-dev:
	pip install -e '.[testing]' --upgrade
