.PHONY: help start stop restart status logs health setup format lint test test-cov clean

# Default target
help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

# Service management
start: ## Start all services
	docker compose up --build -d

stop: ## Stop all services
	docker compose down

restart: ## Recreate services (reloads .env and compose.yml)
	docker compose up --build -d --force-recreate

status: ## Show service status
	docker compose ps

logs: ## Show service logs
	docker compose logs -f


# Development
setup: ## Install Python dependencies
	uv sync

format: ## Format code
	uv run ruff format

lint: ## Lint and type check
	uv run ruff check --fix
	uv run mypy src/

# Cleanup
clean: ## Clean up everything
	docker compose down -v
	docker system prune -f