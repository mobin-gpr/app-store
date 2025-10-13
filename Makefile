# =============================================================================
# Django App Store - Makefile
# =============================================================================
# Convenient commands for development and deployment

.PHONY: help install install-dev install-prod migrate makemigrations createsuperuser shell test run clean docker-build docker-up docker-down docker-logs format lint

# Default target
.DEFAULT_GOAL := help

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)Django App Store - Available Commands$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

# =============================================================================
# Installation
# =============================================================================

install: ## Install base dependencies
	@echo "$(YELLOW)Installing base dependencies...$(NC)"
	pip install -r requirements.txt

install-dev: ## Install development dependencies
	@echo "$(YELLOW)Installing development dependencies...$(NC)"
	pip install -r requirements/development.txt

install-prod: ## Install production dependencies
	@echo "$(YELLOW)Installing production dependencies...$(NC)"
	pip install -r requirements/production.txt

# =============================================================================
# Database
# =============================================================================

migrate: ## Run database migrations
	@echo "$(YELLOW)Running migrations...$(NC)"
	python manage.py migrate

makemigrations: ## Create new migrations
	@echo "$(YELLOW)Creating migrations...$(NC)"
	python manage.py makemigrations

createsuperuser: ## Create a superuser
	@echo "$(YELLOW)Creating superuser...$(NC)"
	python manage.py createsuperuser

collectavatars: ## Collect avatars to database
	@echo "$(YELLOW)Collecting avatars...$(NC)"
	python manage.py collectavatars

# =============================================================================
# Development
# =============================================================================

shell: ## Open Django shell
	python manage.py shell

run: ## Run development server
	@echo "$(GREEN)Starting development server...$(NC)"
	python manage.py runserver

test: ## Run tests
	@echo "$(YELLOW)Running tests...$(NC)"
	pytest

collectstatic: ## Collect static files
	@echo "$(YELLOW)Collecting static files...$(NC)"
	python manage.py collectstatic --noinput

# =============================================================================
# Code Quality
# =============================================================================

format: ## Format code with black and isort
	@echo "$(YELLOW)Formatting code...$(NC)"
	black .
	isort .

lint: ## Run linters
	@echo "$(YELLOW)Running linters...$(NC)"
	flake8 .
	pylint --load-plugins pylint_django **/*.py

# =============================================================================
# Docker
# =============================================================================

docker-build: ## Build Docker images
	@echo "$(YELLOW)Building Docker images...$(NC)"
	docker-compose build

docker-up: ## Start Docker containers
	@echo "$(GREEN)Starting Docker containers...$(NC)"
	docker-compose up -d

docker-down: ## Stop Docker containers
	@echo "$(RED)Stopping Docker containers...$(NC)"
	docker-compose down

docker-logs: ## Show Docker logs
	docker-compose logs -f

docker-shell: ## Open shell in web container
	docker-compose exec web /bin/bash

docker-migrate: ## Run migrations in Docker
	docker-compose exec web python manage.py migrate

docker-makemigrations: ## Create migrations in Docker
	docker-compose exec web python manage.py makemigrations

docker-createsuperuser: ## Create superuser in Docker
	docker-compose exec web python manage.py createsuperuser

docker-prod-build: ## Build production Docker images
	@echo "$(YELLOW)Building production Docker images...$(NC)"
	docker-compose -f docker-compose.prod.yml build

docker-prod-up: ## Start production Docker containers
	@echo "$(GREEN)Starting production Docker containers...$(NC)"
	docker-compose -f docker-compose.prod.yml up -d

docker-prod-down: ## Stop production Docker containers
	@echo "$(RED)Stopping production Docker containers...$(NC)"
	docker-compose -f docker-compose.prod.yml down

# =============================================================================
# Cleanup
# =============================================================================

clean: ## Clean temporary files
	@echo "$(YELLOW)Cleaning temporary files...$(NC)"
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '*.egg-info' -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage

clean-docker: ## Remove all Docker containers, images, and volumes
	@echo "$(RED)Removing all Docker containers, images, and volumes...$(NC)"
	docker-compose down -v
	docker system prune -af

# =============================================================================
# Production Deployment
# =============================================================================

deploy-check: ## Run deployment checks
	@echo "$(YELLOW)Running deployment checks...$(NC)"
	python manage.py check --deploy

prod-setup: install-prod migrate collectstatic ## Setup for production
	@echo "$(GREEN)Production setup complete!$(NC)"

