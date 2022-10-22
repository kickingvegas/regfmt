#!/usr/bin/env bash

source .venv/bin/activate && pip install -r src/regfmt/requirements.txt
cd .venv/bin && ln -s ../../scripts/regfmt . 
