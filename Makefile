# MAXX Project Makefile
# Common development commands

.PHONY: help setup dev test lint format build docker-up docker-down clean docs

# Default target
help:
	@echo "MAXX Project - Available Commands:"
	@echo ""
	@echo "Setup & Development:"
	@echo "  make setup         - Initial project setup"
	@echo "  make dev           - Start development environment"
	@echo "  make dev-stop      - Stop development environment"
	@echo ""
	@echo "Testing & Quality:"
	@echo "  make test          - Run all tests"
	@echo "  make test-python   - Run Python tests"
	@echo "  make test-unity    - Run Unity tests (requires Unity)"
	@echo "  make lint          - Run all linters"
	@echo "  make format        - Format all code"
	@echo "  make typecheck     - Run type checking"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-up     - Start all Docker services"
	@echo "  make docker-down   - Stop all Docker services"
	@echo "  make docker-build  - Build all Docker images"
	@echo "  make docker-logs   - View Docker logs"
	@echo ""
	@echo "Documentation:"
	@echo "  make docs          - Build documentation"
	@echo "  make docs-serve    - Serve documentation locally"
	@echo ""
	@echo "Git & CI/CD:"
	@echo "  make pr            - Create PR for current branch"
	@echo "  make release       - Create release"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean         - Clean build artifacts"
	@echo "  make clean-all     - Clean everything including Docker"

# ===========================================
# SETUP & DEVELOPMENT
# ===========================================

setup:
	@echo "Setting up MAXX project..."
	@cp -n .env.example .env || true
	@echo "Installing Python dependencies..."
	@cd tools/python && pip install -e ".[dev]"
	@echo "Starting Agent Brain..."
	@docker-compose up -d agent-brain
	@echo "Waiting for Agent Brain to be healthy..."
	@until curl -sf http://localhost:3030/health; do sleep 2; done
	@echo "Setup complete!"

dev: docker-up
	@echo "Development environment started"

dev-stop: docker-down

# ===========================================
# TESTING
# ===========================================

test: test-python test-unity

test-python:
	@cd tools/python && pytest --cov=scripts --cov-report=term-missing --cov-report=xml

test-unity:
	@echo "Unity tests require Unity Editor - run manually in Unity"
	@echo "Or use: docker-compose --profile builders up unity-builder"

# ===========================================
# LINTING & FORMATTING
# ===========================================

lint: lint-python lint-markdown lint-yaml lint-docker

lint-python:
	@cd tools/python && ruff check scripts

lint-markdown:
	@markdownlint docs/**/*.md README.md

lint-yaml:
	@yamllint .github/workflows/ docker-compose.yml

lint-docker:
	@hadolint infrastructure/docker/Dockerfile.*

format:
	@cd tools/python && ruff format scripts
	@cd tools/python && isort scripts

typecheck:
	@cd tools/python && mypy scripts

# ===========================================
# DOCKER
# ===========================================

docker-up:
	@docker-compose up -d

docker-down:
	@docker-compose down --remove-orphans

docker-build:
	@docker-compose build --no-cache

docker-logs:
	@docker-compose logs -f

docker-ps:
	@docker-compose ps

# Start specific profiles
docker-agents:
	@docker-compose --profile agents up -d

docker-workers:
	@docker-compose --profile workers up -d

docker-builders:
	@docker-compose --profile builders up -d

docker-database:
	@docker-compose --profile database up -d

docker-monitoring:
	@docker-compose --profile monitoring up -d

# ===========================================
# DOCUMENTATION
# ===========================================

docs:
	@cd tools/python && mkdocs build --site-dir ../../docs/_build

docs-serve:
	@cd tools/python && mkdocs serve --dev-addr 0.0.0.0:8000

# ===========================================
# GIT & CI/CD
# ===========================================

pr:
	@branch=$$(git branch --show-current); \
	if [ "$$branch" = "main" ] || [ "$$branch" = "dev" ]; then \
		echo "Cannot create PR from $$branch branch"; \
		exit 1; \
	fi; \
	gh pr create --fill --base dev

release:
	@version=$$(cat VERSION 2>/dev/null || echo "0.1.0"); \
	new_version=$$(echo $$version | awk -F. '{$$NF+=1; print $$1"."$$2"."$$3}'); \
	echo $$new_version > VERSION; \
	git add VERSION; \
	git commit -m "chore: release v$$new_version"; \
	git tag v$$new_version; \
	git push origin main --tags

# ===========================================
# CLEANUP
# ===========================================

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@rm -rf tools/python/.coverage tools/python/htmlcov 2>/dev/null || true
	@rm -rf docs/_build 2>/dev/null || true

clean-all: clean
	@docker-compose down -v --remove-orphans 2>/dev/null || true
	@docker system prune -f 2>/dev/null || true
	@rm -rf .venv venv env 2>/dev/null || true

# ===========================================
# AGENT BRAIN
# ===========================================

agent-brain-start:
	@docker-compose up -d agent-brain

agent-brain-logs:
	@docker-compose logs -f agent-brain

agent-brain-health:
	@curl -sf http://localhost:3030/health && echo "OK" || echo "FAILED"

# ===========================================
# QUICK COMMANDS
# ===========================================

quick-start: setup docker-agents docker-workers
	@echo "Quick start complete! Agents and workers running."

status:
	@echo "=== Git Status ===" && git status --short
	@echo "" && echo "=== Docker Status ===" && docker-compose ps
	@echo "" && echo "=== Agent Brain ===" && curl -sf http://localhost:3030/health && echo "OK" || echo "NOT RUNNING"

# ===========================================
# UNITY (requires Unity installed)
# ===========================================

unity-build:
	@docker-compose --profile builders run --rm unity-builder

unity-test:
	@docker-compose --profile builders run --rm unity-builder unity -batchmode -runTests -projectPath /project -testResults /builds/test-results.xml -logfile -

unity-editor:
	@echo "Open Unity Hub and load project from ./src"