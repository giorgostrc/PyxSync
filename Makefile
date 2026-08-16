.PHONY: pip-tools compile compile-dev install install-dev lint

pip-tools:
	pip install pip-tools

compile:
	pip-compile requirements.in -o requirements.txt

compile-dev:
	pip-compile dev-requirements.in -c requirements.txt -o dev-requirements.txt

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt -r dev-requirements.txt

lint:
	pre-commit run --all-files
