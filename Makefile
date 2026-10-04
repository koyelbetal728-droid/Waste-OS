.PHONY: up down test migrate seed train train-detect train-cnn evaluate

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
	python -m scripts.train_models

train-detect:
	python -m scripts.train_yolo_detect

train-cnn:
	python -m scripts.train_cnn_classifier

evaluate:
	python -m scripts.evaluate_models
