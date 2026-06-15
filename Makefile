PYTHON ?= python3
VENV ?= .venv
PIP := $(VENV)/bin/pip
PYTEST := $(VENV)/bin/pytest
RUFF := $(VENV)/bin/ruff
UVICORN := $(VENV)/bin/uvicorn

.PHONY: setup test lint run eval docker-build docker-run clean

setup:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -e ".[dev]"

test:
	PYTHONPATH=src:. $(PYTEST)

lint:
	$(RUFF) check src tests app

run:
	PYTHONPATH=src:. $(UVICORN) app.main:app --host 0.0.0.0 --port 8080

eval:
	PYTHONPATH=src:. $(VENV)/bin/llm-eval-gateway evaluate --model candidate --output reports/latest.json

docker-build:
	docker build -f infra/docker/Dockerfile -t llm-eval-regression-gateway:local .

docker-run:
	docker run --rm -p 8080:8080 llm-eval-regression-gateway:local

clean:
	rm -rf $(VENV) .pytest_cache .ruff_cache build dist *.egg-info reports/*.json
