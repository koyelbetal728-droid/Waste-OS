"""Prints the current registry state — what's trained, what's in
production, and its real evaluation metrics."""
from packages.ml.model_registry.registry import list_versions, get_production_model

MODELS = ["waste-classifier", "waste-forecast"]


def main():
    for name in MODELS:
        print(f"\n=== {name} ===")
        versions = list_versions(name)
        if not versions:
            print("No versions trained yet.")
            continue
        for v in versions:
            marker = " (PRODUCTION)" if v["status"] == "production" else ""
            print(f"{v['version']}{marker}: {v['metrics']}")


if __name__ == "__main__":
    main()
