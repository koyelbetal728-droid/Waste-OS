.PHONY: up down test migrate seed

up:
	docker compose up --build

down:
	docker compose down

test:
	docker compose exec api pytest tests/unit -v

migrate:
	docker compose exec api alembic -c db/migrations/alembic.ini upgrade head

seed:
	docker compose exec api python -m db.seeds.dev_accounts

train:
	docker compose exec api python -m scripts.train_models
