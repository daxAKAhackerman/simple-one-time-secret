SHELL := /usr/bin/env bash

MONGO_USER = user
MONGO_DB = secret
#MONGO_PASSWORD := $(shell cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)\n

install:
	@python3 -m pip install pipenv -U
	@pipenv install --dev
	@pipenv run pre-commit install
	@npm install --prefix client

generate-secrets:
ifeq ($(wildcard ./.env),)
	@echo MONGO_USER=$(MONGO_USER) >> .env
	@echo MONGO_DB=$(MONGO_DB) >> .env
	@echo MONGO_PASSWORD=$(MONGO_PASSWORD) >> .env
else
	@echo "[-] Docker environment variables are already set"
endif

test:
	@pipenv run pytest

test-coverage-report:
	@pipenv run pytest -v --cov=server --cov-report html:cov_html

run-pre-commit:
	@pipenv run pre-commit run -a

#run-local: run-pre-commit
run-local:
	@cd server && pipenv run uvicorn main:app --reload
