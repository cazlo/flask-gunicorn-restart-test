# Makefile

.PHONY: help build up down logs shell clean test dev wait-for-health loadtest loadtest-web

# Default target executed when no arguments are given to make.
help:
	@echo "Available targets:"
	@echo "  build     - Build the Docker images"
	@echo "  up        - Start the application"
	@echo "  down      - Stop the application"
	@echo "  logs      - View logs"
	@echo "  shell     - Enter the web container shell"
	@echo "  clean     - Remove containers and volumes"
	@echo "  test      - Run tests"
	@echo "  dev       - Run in development mode without Docker"
	@echo "  wait-for-health - Wait until application is healthy"
	@echo "  loadtest  - Run load test in headless mode (10 RPS for 60 seconds)"
	@echo "  loadtest-web - Run load test with web UI"

# Build Docker images
build:
	docker compose build

# Start the application
up:
	docker compose up -d

# Start the application and show logs
up-logs:
	docker compose up

# Stop the application
down:
	docker compose down

# View logs
logs:
	docker compose logs -f

# Enter the web container shell
shell:
	docker compose exec web bash

# Remove containers and volumes
clean:
	docker compose down -v

# Run tests (can be expanded later)
test:
	docker compose run --rm web pytest

# Run in development mode without Docker
dev:
	pip install -r requirements.txt
	python run_dev.py

# Install dependencies
install:
	pip install -r requirements.txt

# Check health
health:
	curl http://localhost:8000/health

# Wait for the application to become healthy
wait-for-health:
	@echo "Waiting for application to become healthy..."
	@until docker compose exec web curl -s http://localhost:8000/health | grep -q '"status":"healthy"'; do \
		echo "Waiting for health check to pass..."; \
		sleep 2; \
	done
	@echo "Application is healthy!"

# Run load test in headless mode (10 RPS for 60 seconds)
loadtest:
	@echo "Running load test at 10 requests per second for 60 seconds..."
	locust -f locustfile.py --headless -u 20 -r 2 -t 60s --host=http://localhost:8000

# Run load test with web UI
loadtest-web:
	@echo "Starting Locust web interface..."
	locust -f locustfile.py --host=http://localhost:8000

# Run database migrations (placeholder for future use)
migrate:
	@echo "Running migrations..."
	# Add migration commands here when needed