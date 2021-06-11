CODE = src
TESTS = tests

ALL = $(CODE) $(TESTS)

VENV ?= venv

venv:
	sudo python3.8 -m venv $(VENV)
	$(VENV)/bin/python3.8 -m pip install --upgrade pip
	$(VENV)/bin/python3.8 -m pip install poetry
	$(VENV)/bin/poetry install
	source $(VENV)/bin/activate

# for Windows:
win_venv:
	python -m venv $(VENV)
	$(VENV)\Scripts\python -m pip install --upgrade pip
	$(VENV)\Scripts\python -m pip install poetry
	$(VENV)\Scripts\poetry install


setup:
	$(VENV)/bin/python setup.py install


test:
	$(VENV)/bin/pytest -v tests


win_test:
	$(VENV)\Scripts\pytest -v tests


up:
	python3.8 -m aiohttp.web -H localhost -P 8080 $(CODE).main:init_func


ci:	lint test


win_ci: win_lint win_test


.PHONY: venv