PYTHON ?= python3
PIP ?= pip3

.PHONY: install run lint test ci up down

install:
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

lint:
	ruff check .

test:
	PYTHONPATH=. pytest

ci: lint test

up:
	docker compose up --build -d

down:
	docker compose down
