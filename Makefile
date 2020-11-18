.PHONY: test
test: development
	venv/bin/tox

.PHONY: development
development: requirements-dev-minimal.txt venv/bin/activate
venv/bin/activate:
	test -d venv || python3 -m venv venv
	venv/bin/pip install -r requirements-dev-minimal.txt
	pre-commit install
	touch venv/bin/activate
