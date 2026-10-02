"""Orchestrates training across all trainable models. Run inside a
container with the ML deps installed (the api/worker images already have
them):

    docker compose exec api python -m scripts.train_models

Each trainer prints why it skipped if there isn't enough data yet — it
never fabricates a "trained" model from nothing.
"""
from packages.ml.classification.train import train as train_classifier


def main():
    print("=== Waste classifier ===")
    train_classifier()
    print("\nForecasting: call packages.ml.forecasting.train.train(history) "
          "directly with your real historical waste totals — there's no "
          "bundled time-series dataset to auto-load here.")


if __name__ == "__main__":
    main()
