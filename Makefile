EXEC=regfmt
EXEC_SRC=${EXEC}.py

help:
	./${EXEC_SRC} -h

test:
	python -m unittest discover

.PHONY: help test
