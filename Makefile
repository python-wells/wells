PYTHON_MODULES = wells
PYTHONPATH = .
VENV = .venv
PYTHON = env PYTHONPATH=$(PYTHONPATH) $(VENV)/bin/python
PIP = env PYTHONPATH=$(PYTHONPATH) $(VENV)/bin/pip
PYTEST = env PYTHONPATH=$(PYTHONPATH) PYTEST=1 $(VENV)/bin/py.test
PYLINT = env PYTHONPATH=$(PYTHONPATH) $(VENV)/bin/pylint --disable=missing-docstring,invalid-name,global-statement --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}"
PEP8 = env PYTHONPATH=$(PYTHONPATH) $(VENV)/bin/pycodestyle --repeat --ignore=E202,E501,W504

default: test
dist: bootstrap
	rm -rf dist/*
	$(PYTHON) setup.py -q sdist
	$(PYTHON) setup.py -q bdist_wheel --universal
upload: dist
	$(VENV)/bin/twine upload dist/*
build:

bootstrap:
	test -d $(VENV) || python3 -m venv $(VENV) || python2 -m virtualenv -q $(VENV)
	$(PIP) install -q -r requirements-dev.txt
check: test
pylint: bootstrap
	$(PEP8) $(PYTHON_MODULES)
	$(PYLINT) -E $(PYTHON_MODULES)
pylint-full: pylint
	$(PYLINT) $(PYTHON_MODULES)
test: pylint
	$(PYTEST) $(PYTHON_MODULES)
tox:
	$(VENV)/bin/tox
install-git-hooks:
	utils/install-git-hooks
clean:
	find . -name "__pycache__" -type d -exec rm -rf {} \;
	find . -name "*.pyc" -type f -exec rm -rf {} \;
TAGS:
	etags -R --exclude=static $(PYTHON_MODULES)
loc:
	cloc wells
.PHONY: default dist upload build bootstrap check pylint pylint-full test tox install-git-hooks clean TAGS loc
