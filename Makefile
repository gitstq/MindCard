# MindCard - Makefile

.PHONY: help install test lint clean build dist upload

PYTHON := python3
PIP := pip3

help:
	@echo "MindCard - Available Commands"
	@echo "=============================="
	@echo "make install    - Install MindCard locally"
	@echo "make test       - Run unit tests"
	@echo "make clean      - Clean build artifacts"
	@echo "make build      - Build distribution packages"
	@echo "make dist       - Create source and wheel distributions"

install:
	$(PIP) install -e . --break-system-packages

test:
	$(PYTHON) -m pytest tests/ -v
	# Fallback to unittest if pytest not available
	$(PYTHON) -m unittest tests.test_mindcard -v

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

build: clean
	$(PYTHON) setup.py sdist bdist_wheel

dist: build
	@echo "Distribution packages created in dist/"

run:
	$(PYTHON) mindcard.py

dev:
	$(PYTHON) mindcard.py dashboard
