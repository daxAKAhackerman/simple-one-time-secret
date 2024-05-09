SHELL := /usr/bin/env bash
SRC_SERVER_DIR := server
SRC_CLIENT_DIR := client

install:
	@python3 -m pip install pipenv -U
	@python3 -m pipenv install --dev
	@python3 -m pipenv run pre-commit install
	@npm install --prefix client

lock-requirements:
	@python3 -m pipenv requirements > $(SRC_SERVER_DIR)/requirements.txt

lint:
	@python3 -m pipenv run black --line-length=160 $(SRC_SERVER_DIR)
	@python3 -m pipenv run isort --profile black $(SRC_SERVER_DIR)

test:
	@pipenv run pytest

test-coverage-report:
	@pipenv run pytest --cov-report term-missing --cov=server server/tests/

run-backend:
	@cd $(SRC_SERVER_DIR) && python3 -m pipenv run uvicorn main:app --reload

run-database:
	@docker run -p 27017:27017 --rm mongo:7.0

run-web-app:
	@npm --prefix client run serve

deploy: generate-secrets
	@docker-compose build
	@docker-compose up -d

update:
	@docker-compose build
	@docker-compose up -d

start:
	@docker-compose up -d

stop:
	@docker-compose down
