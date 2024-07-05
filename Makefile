MODULE = lazystuff

ifeq ($(ENV),)
	FLAKE	   ?= flake8
	MYPY	   ?= mypy
	PYDOCSTYLE ?= pydocstyle
	PYLINT	   ?= $(shell type pylint3 > /dev/null 2>&1 && echo "pylint3" || echo "pylint")
	PYTEST	   ?= pytest
	PYTHON	   ?= python
	SPHINX	   ?= sphinx-build
	VULTURE	   ?= vulture
else
	PYLINT	   ?= $(shell realpath $(ENV)/bin)/pylint
	VULTURE	   ?= $(shell realpath $(ENV)/bin)/vulture
	MYPY	   ?= $(shell realpath $(ENV)/bin)/mypy
	PYDOCSTYLE ?= $(shell realpath $(ENV)/bin)/pydocstyle
	FLAKE	   ?= $(shell realpath $(ENV)/bin)/flake8
	PYTEST	   ?= $(shell realpath $(ENV)/bin)/pytest
	PYTHON	   ?= $(shell realpath $(ENV)/bin)/python
	SPHINX	   ?= $(shell realpath $(ENV)/bin)/sphinx-build
endif


.PHONY: lint check build test doc clean

doc:
	(cd doc && make SPHINXBUILD=$(SPHINX) html)

README.md: doc/conf.py doc/index.rst
	(cd doc && make SPHINXBUILD=$(SPHINX) markdown)
	cp doc/_build/markdown/index.md README.md

build: README.md
	$(PYTHON) -m build

check: lint test

lint: vulture flake8 pydocstyle pylint mypy

pylint: pyproject.toml
	$(PYLINT) $(MODULE)

flake8: pyproject.toml
	$(FLAKE) $(MODULE)

pydocstyle: pyproject.toml
	$(PYDOCSTYLE) --convention pep257 $(MODULE)

mypy: pyproject.toml
	$(MYPY) $(MODULE)

vulture: pyproject.toml
	$(VULTURE) $(MODULE) .vulture-whitelist

test: pyproject.toml
	PYTHONPATH=. $(PYTEST)

clean:
	find . -name '*~' -exec rm '{}' ';'
	rm -rf deb_dist dist *.egg-info build
