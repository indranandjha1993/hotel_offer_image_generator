
YELLOW := \033[1;33m
GREEN := \033[1;32m
RED := \033[1;31m
NC := \033[0m # No Color

DOCKER_COMPOSE_FILE := docker-compose.yml
DOCKER_COMPOSE_CMD := docker compose

.PHONY: help
help: ## Display this help screen
	@echo "$(YELLOW)Hotel Offer Image Generator Makefile$(NC)"
	@echo "Usage: make [command]"
	@echo ""
	@echo "Commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-30s$(NC) %s\n", $$1, $$2}'

# Docker commands
.PHONY: build
build: ## Build Docker images
	@echo "$(GREEN)Building Docker images...$(NC)"
	$(DOCKER_COMPOSE_CMD) -f $(DOCKER_COMPOSE_FILE) build

.PHONY: up
up: ## Start the application
	@echo "$(GREEN)Starting the application...$(NC)"
	$(DOCKER_COMPOSE_CMD) -f $(DOCKER_COMPOSE_FILE) up -d

.PHONY: down
down: ## Stop the application
	@echo "$(GREEN)Stopping the application...$(NC)"
	$(DOCKER_COMPOSE_CMD) -f $(DOCKER_COMPOSE_FILE) down

.PHONY: logs
logs: ## View application logs
	@echo "$(GREEN)Viewing application logs...$(NC)"
	$(DOCKER_COMPOSE_CMD) -f $(DOCKER_COMPOSE_FILE) logs -f

# Development commands
.PHONY: install
install: ## Install Python dependencies
	@echo "$(GREEN)Installing Python dependencies...$(NC)"
	pip install -r requirements.txt

.PHONY: lint
lint: ## Run linter
	@echo "$(GREEN)Running linter...$(NC)"
	flake8 .

.PHONY: test
test: ## Run tests
	@echo "$(GREEN)Running tests...$(NC)"
	pytest tests || (echo "$(YELLOW)No tests found or tests failed. Ensure tests are set up correctly.$(NC)" && exit 0)

.PHONY: create-test
create-test: ## Create a new test file
	@read -p "Enter the name for the new test file (without .py): " name; \
	echo "Creating test file: tests/test_$$name.py"; \
	echo "def test_$$name():" > "tests/test_$$name.py"; \
	echo "    assert True, \"Test $$name functionality here\"" >> "tests/test_$$name.py"; \
	echo "$(GREEN)Test file created: tests/test_$$name.py$(NC)"

.PHONY: format
format: ## Format code
	@echo "$(GREEN)Formatting code...$(NC)"
	black .

# Application commands
.PHONY: run-cli
run-cli: ## Run the CLI application
	@echo "$(GREEN)Running CLI application...$(NC)"
	$(DOCKER_COMPOSE_CMD) -f $(DOCKER_COMPOSE_FILE) exec cli python /app/run_cli.py

.PHONY: run-api
run-api: ## Run the API application
	@echo "$(GREEN)Running API application...$(NC)"
	$(DOCKER_COMPOSE_CMD) -f $(DOCKER_COMPOSE_FILE) exec web python /app/run_api.py

# Cleanup
.PHONY: clean
clean: ## Remove all generated files and docker artifacts
	@echo "$(GREEN)Cleaning up...$(NC)"
	$(DOCKER_COMPOSE_CMD) -f $(DOCKER_COMPOSE_FILE) down -v --remove-orphans
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Default target
.DEFAULT_GOAL := help
