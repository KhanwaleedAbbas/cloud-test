.PHONY: up down rebuild logs ps fmt lint test clean

up:
	docker compose up -d --build

down:
	docker compose down -v

rebuild:
	docker compose build --no-cache

logs:
	docker compose logs -f | cat

ps:
	docker compose ps

fmt:
	@echo "Formatting is handled per-service (e.g., black)."

lint:
	@echo "Linting is handled per-service (e.g., flake8/ruff)."

test:
	@echo "Tests run per-service (pytest)."

clean:
	git clean -fdx -e .env

