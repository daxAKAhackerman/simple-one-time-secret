SHELL := /usr/bin/env bash

MONGO_USR = user
MONGO_PWD := $(shell cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)\n

install:
	@python3 -m pip install pipenv -U
	@pipenv install --dev
	@pipenv run pre-commit install
	@npm install --prefix client

generate-secrets:
ifeq ($(wildcard ./.env),)
	@echo MONGO_USER=$(MONGO_USR) >> .env
	@echo MONGO_PASSWORD=$(MONGO_PWD) >> .env
else
	@echo "[-] Docker environment variables are already set"
endif

lint:
	@pipenv run black --line-length=160 server
	@pipenv run isort --profile black server

test:
	@pipenv run pytest

test-coverage-report:
	@pipenv run pytest --cov-report term-missing --cov=server server/tests/

run-local:
run-local:
	@cd server && pipenv run uvicorn main:app --reload
