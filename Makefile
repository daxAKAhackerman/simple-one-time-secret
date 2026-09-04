SHELL := /usr/bin/env bash
SRC_SERVER_DIR := server
SRC_CLIENT_DIR := client
TEST_DIR := $(SRC_SERVER_DIR)/tests

.PHONY: build start stop install lock-requirements lint test test-coverage-report run-backend build-frontend run-frontend run-database

build:
	docker volume create simpleonetimesecret-db
	docker build -t simpleonetimesecret -f docker/Dockerfile .

install:
	python3 -m pip install pipenv -U
	python3 -m pipenv install --dev
	python3 -m pipenv run pre-commit install
	npm install --prefix $(SRC_CLIENT_DIR)

lock-requirements:
	python3 -m pipenv requirements > $(SRC_SERVER_DIR)/requirements.txt

lint:
	python3 -m pipenv run black --line-length=160 $(SRC_SERVER_DIR)
	python3 -m pipenv run isort --profile black $(SRC_SERVER_DIR)
	npm run --prefix $(SRC_CLIENT_DIR) lint
	npm run --prefix $(SRC_CLIENT_DIR) format

test:
	python3 -m pipenv run pytest $(TEST_DIR)

test-coverage-report:
	python3 -m pipenv run pytest --cov-report term-missing --cov=$(SRC_SERVER_DIR) $(TEST_DIR)

run-backend:
	cd $(SRC_SERVER_DIR) && python3 -m pipenv run uvicorn main:app --reload

build-frontend:
	npm run --prefix $(SRC_CLIENT_DIR) build

run-frontend:
	npm run --prefix $(SRC_CLIENT_DIR) dev

run-database:
	docker run -p 27017:27017 --rm mongo:7.0

start:
	docker run -p 8080:80 -v simpleonetimesecret-db:/data/db -d --name simpleonetimesecret simpleonetimesecret

stop:
	docker stop simpleonetimesecret
	docker rm simpleonetimesecret
