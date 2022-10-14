SHELL := /opt/local/bin/bash
EXEC=regfmt
EXEC_SRC=${EXEC}.py
PYTHON_EXEC=python3

help:
	./${EXEC_SRC} -h

test:
	python -m unittest discover

clean:
	find . -name '*.*~' -print -exec rm {} \;


install: .venv
	source .venv/bin/activate && pip install -r requirements.txt
	cd .venv/bin && ln -s ../../regfmt.py regfmt

.venv:
	${PYTHON_EXEC} -m venv .venv

install-pip-requirements:
	pip install -r requirements.txt

freeze-pip-requirements:
	pip freeze > requirements.txt

deep-clean: clean
	find . -name '__pycache__' -not -path "./.venv/*" -print | xargs rm -rf 

clean-tests:
	make -C tests clean

.PHONY: help test clean deep-clean clean-tests install-pip-requirements freeze-pip-requirements
