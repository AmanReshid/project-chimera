# Makefile for common developer and CI commands

IMAGE_NAME ?= project-chimera
PY_VERSION ?= 3.14-slim

.PHONY: help build build-fast build-ci test install setup security-check docker-run docker-test spec-check clean

help:
	@echo "Usage: make <target>"
	@echo "Targets:"
	@echo "  build        Build image and run tests during build (CI-style)"
	@echo "  build-fast   Build image but skip tests during build (faster)"
	@echo "  build-ci     Alias for build (keeps CI naming)"
	@echo "  test         Run test suite locally with pytest"
	@echo "  install      Install package into local env (editable)"
	@echo "  docker-run   Run the runtime image interactively"
	@echo "  clean        Remove local images produced by this Makefile"

build:
	docker build -t $(IMAGE_NAME):ci --build-arg PYTHON_VERSION=$(PY_VERSION) --build-arg RUN_TESTS=true .

build-fast:
	docker build -t $(IMAGE_NAME):latest --build-arg PYTHON_VERSION=$(PY_VERSION) --build-arg RUN_TESTS=false .

build-ci: build

test:
	pytest -q

install:
	python -m pip install -e .

# setup: create a local virtualenv in .venv and install dependencies there
# Works on POSIX and Windows (uses Scripts\pip.exe when present)
setup:
	python -m venv .venv
	@sh -c 'if [ -f .venv/bin/pip ]; then P=.venv/bin/pip; else P=.venv/Scripts/pip.exe; fi; \
	$$P install --upgrade pip setuptools wheel; \
	$$P install -e .'

docker-run:
	docker run --rm -it $(IMAGE_NAME):latest /bin/sh

# docker-test: build the builder stage and run the test suite inside it.
# This will fail the build if tests fail and print pytest output in build logs.
docker-test:
	docker build --target builder -t $(IMAGE_NAME):test --build-arg PYTHON_VERSION=$(PY_VERSION) --build-arg RUN_TESTS=true .

spec-check:
	python scripts/spec_check.py

security-check:
	python -m pip install --upgrade pip
	python -m pip install bandit pip-audit
	# Run Bandit (static security analysis)
	bandit -r . -f txt
	# Run pip-audit and fail build on high severity vulnerabilities
	pip-audit --format json --output pip-audit.json --fail-on high

clean:
	-docker rmi $(IMAGE_NAME):ci $(IMAGE_NAME):latest || true
