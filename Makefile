# MAXX Project Makefile
# Common development commands

.PHONY: help setup dev test build docs clean deploy lint

# Default target
help:
	@echo "MAXX - AI-Orchestrated Unity Game Development"
	@echo ""
	@echo "Available commands:"
	@echo "  setup       - Initial project setup"
	@echo "  dev         - Start development environment"
	@echo "  test        - Run all tests"
	@echo "  build       - Build Unity project"
	@echo "  docs        - Generate documentation"
	@echo "  lint        - Run linters"
	@echo "  clean       - Clean build artifacts"
	@echo "  deploy      - Deploy to staging"
	@echo "  agents      - Start agent runners"
	@echo "  workers     - Start generation workers"
	@echo "  infra       - Start infrastructure only"
	@echo "  logs        - View service logs"
	@echo "  status      - Show service status"
	@echo "  checkpoint  - Create a checkpoint"

# ========================================
# SETUP
# ========================================
setup:
	@echo "Setting up MAXX project..."
	cp -n .env.example .env || true
	docker-compose pull
	docker-compose build
	pip install -e tools/python
	@echo "Setup complete! Edit .env with your API keys."

# ========================================
# DEVELOPMENT
# ========================================
dev: infra agents workers
	@echo "Development environment started!"

infra:
	docker-compose up -d agent-brain postgres redis

agents:
	docker-compose --profile agents up -d

workers:
	docker-compose --profile workers up -d

builders:
	docker-compose --profile builders up -d

database:
	docker-compose --profile database up -d

monitoring:
	docker-compose --profile monitoring up -d

# ========================================
# TESTING
# ========================================
test:
	@echo "Running all tests..."
	cd tools/python && pytest --cov=scripts --cov-report=term-missing
	@echo "Python tests done"

test-unit:
	cd tools/python && pytest -m unit --cov=scripts --cov-report=term-missing

test-integration:
	cd tools/python && pytest -m integration

test-agent:
	cd tools/python && pytest -m agent

# ========================================
# BUILD
# ========================================
build:
	@echo "Building Unity project..."
	docker-compose --profile builders run --rm unity-builder

build-docker:
	docker-compose build

# ========================================
# DOCUMENTATION
# ========================================
docs:
	@echo "Generating documentation..."
	cd tools/python && mkdocs build --site-dir ../../docs/generated

docs-serve:
	cd tools/python && mkdocs serve

# ========================================
# LINTING
# ========================================
lint:
	@echo "Running linters..."
	cd tools/python && ruff check scripts
	cd tools/python && ruff format --check scripts
	cd tools/python && mypy scripts
	markdownlint docs/**/*.md README.md

lint-fix:
	cd tools/python && ruff check --fix scripts
	cd tools/python && ruff format scripts

# ========================================
# CLEANUP
# ========================================
clean:
	@echo "Cleaning build artifacts..."
	docker-compose down -v --remove-orphans
	docker system prune -f
	rm -rf builds/*
	rm -rf tools/python/.pytest_cache
	rm -rf tools/python/.mypy_cache
	rm -rf tools/python/.ruff_cache
	rm -rf tools/python/htmlcov
	rm -rf tools/python/dist
	rm -rf tools/python/build
	rm -rf tools/python/*.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true

# ========================================
# DEPLOYMENT
# ========================================
deploy-staging:
	@echo "Deploying to staging..."
	gh workflow run cd.yml -f environment=staging

deploy-production:
	@echo "Deploying to production..."
	gh workflow run cd.yml -f environment=production

# ========================================
# UTILITIES
# ========================================
logs:
	docker-compose logs -f

logs-agent-brain:
	docker-compose logs -f agent-brain

logs-claude:
	docker-compose logs -f claude-code-runner

logs-codex:
	docker-compose logs -f codex-runner

logs-meshy:
	docker-compose logs -f meshy-worker

logs-minimax:
	docker-compose logs -f minimax-worker

status:
	docker-compose ps

restart:
	docker-compose restart

down:
	docker-compose down

down-volumes:
	docker-compose down -v

# ========================================
# CHECKPOINTS
# ========================================
checkpoint:
	@read -p "Checkpoint question: " question; \
	read -p "Options (comma-separated): " options; \
	python -c "
from tools.python.scripts.agent_brain.checkpoint_manager import CheckpointManager
mgr = CheckpointManager()
result = mgr.create_checkpoint(question=question, options=options.split(','))
print(f'Result: {result.status.value} - {result.response}')
"

# ========================================
# GITHUB
# ========================================
pr-create:
	@read -p "PR title: " title; \
	read -p "PR body: " body; \
	read -p "Branch: " branch; \
	python -c "
from tools.python.scripts.github_automation.github_client import GitHubClient
client = GitHubClient()
pr = client.create_pr(title=title, body=body, head_branch=branch)
print(f'PR created: {pr}')
"

# ========================================
# AGENT BRAIN
# ========================================
memory-read:
	python -c "
from tools.python.scripts.agent_brain.memory_client import AgentBrainClient
client = AgentBrainClient()
memory = client.read_memory()
print(memory)
"

memory-write:
	@read -p "Content to write: " content; \
	python -c "
from tools.python.scripts.agent_brain.memory_client import AgentBrainClient
client = AgentBrainClient()
result = client.write_memory(content=content)
print(result)
"

# ========================================
# QUICK START
# ========================================
quickstart: setup dev
	@echo ""
	@echo "MAXX is running!"
	@echo "  Agent Brain: http://localhost:3030"
	@echo "  Grafana: http://localhost:3000 (if monitoring enabled)"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Edit .env with your API keys"
	@echo "  2. Run 'make checkpoint' to create your first checkpoint"
	@echo "  3. Start Unity: open src/ in Unity Hub"