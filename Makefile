##
# Copyright 2022 Charles Y. Choi
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

EXEC=regfmt
EXEC_SRC=${EXEC}.py
PYTHON_EXEC=python3

help:
	./scripts/${EXEC} -h

test:
	python -m unittest discover

clean:
	find . -name '*.*~' -print -exec rm {} \;

install: .venv
	./scripts/install.sh

.venv:
	${PYTHON_EXEC} -m venv .venv

install-pip-requirements:
	pip install -r src/regfmt/requirements.txt

freeze-pip-requirements:
	pip freeze > src/regfmt/requirements.txt

deepclean: clean
	find . -name '__pycache__' -not -path "./.venv/*" -print | xargs rm -rf
	rm -rf dist

clean-tests:
	make -C tests clean

readme-examples:
	regfmt -s tests/data/github.css -o tests/control/example_0001.svg tests/data/example_0001.yaml
	regfmt -s tests/data/github.css -o tests/control/register.svg tests/data/register.yaml
	regfmt -s tests/data/github.css -o tests/control/register-stair-left.svg tests/data/register-stair-left.yaml


package:
	${PYTHON_EXEC} -m build

upload:
	twine upload --repository pypi dist/*

.PHONY: help test clean deepclean clean-tests install-pip-requirements freeze-pip-requirements readme-examples package upload
