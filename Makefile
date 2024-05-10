SHELL := /usr/bin/env bash
SRC_SERVER_DIR := server
SRC_CLIENT_DIR := client
TEST_DIR := $(SRC_SERVER_DIR)/tests

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
	@python3 -m pipenv run pytest $(TEST_DIR)

test-coverage-report:
	@python3 -m pipenv run pytest --cov-report term-missing --cov=$(SRC_SERVER_DIR) $(TEST_DIR)

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
