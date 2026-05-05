compile:
	pip-compile requirements.in -o requirements.txt

compile-dev:
	pip-compile dev-requirements.in -c requirements.txt -o dev-requirements.txt

lint:
	pre-commit run --all-files
