PYTHON := python3
VENV := .venv
BIN := $(VENV)/bin

.PHONY: setup evaluate test lint run docker-build

setup:
	$(PYTHON) -m venv $(VENV)
	$(BIN)/pip install --upgrade pip
	$(BIN)/pip install -r requirements.txt

evaluate:
	PYTHONPATH=. $(BIN)/python scripts/run_eval.py

test:
	PYTHONPATH=. $(BIN)/pytest

lint:
	$(BIN)/ruff check .

run:
	PYTHONPATH=. $(BIN)/uvicorn app.main:app --host 0.0.0.0 --port 8000

docker-build:
	docker build -f infra/docker/Dockerfile -t llm-eval-regression-gateway:local .
