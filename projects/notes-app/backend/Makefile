.PHONY: help install dev test lint clean

help:
	@echo "Notes Backend - Available Commands"
	@echo "=================================="
	@echo "  make install    Install dependencies via pip"
	@echo "  make install-poetry Install dependencies via poetry"
	@echo "  make dev        Run development server with auto-reload"
	@echo "  make test       Run all tests"
	@echo "  make test-cov   Run tests with coverage report"
	@echo "  make clean      Remove __pycache__ and .pytest_cache"
	@echo "  make lint       Run Python syntax check"

install:
	pip install -r requirements.txt

install-poetry:
	poetry install

dev:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest -v

test-cov:
	pytest --cov=app --cov-report=html tests/

lint:
	python3 -m py_compile app/*.py tests/*.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -f .coverage
	rm -rf htmlcov/
