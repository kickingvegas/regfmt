EXEC=regfmt
EXEC_SRC=${EXEC}.py

help:
	./${EXEC_SRC} -h

test:
	python -m unittest discover

clean:
	find . -name '*.*~' -print -exec rm {} \;

install-pip-requirements:
	pip install -r requirements.txt

freeze-pip-requirements:
	pip freeze > requirements.txt

deep-clean: clean
	find . -name '__pycache__' -not -path "./.venv/*" -print | xargs rm -rf 

clean-tests:
	make -C tests clean

.PHONY: help test clean deep-clean clean-tests install-pip-requirements freeze-pip-requirements
