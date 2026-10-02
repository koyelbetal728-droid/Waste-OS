"""File-based model registry (real, working — no external MLOps dependency
required). Backed by models/registry/registry.json. Promote/rollback update
the same file so `get_production_model` always reflects the current state."""
import json
import os
from datetime import datetime
from pathlib import Path

REGISTRY_PATH = Path(__file__).resolve().parents[3] / "models" / "registry" / "registry.json"


def _load() -> dict:
    if not REGISTRY_PATH.exists():
        return {}
    with open(REGISTRY_PATH) as f:
        return json.load(f)


def _save(data: dict):
    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(REGISTRY_PATH, "w") as f:
        json.dump(data, f, indent=2)


def register_model(name: str, version: str, artifact_path: str, metrics: dict, dataset_version: str | None = None) -> dict:
    data = _load()
    entry = {
        "version": version,
        "artifact_path": artifact_path,
        "metrics": metrics,
        "dataset_version": dataset_version,
        "status": "staging",
        "created_at": datetime.utcnow().isoformat(),
    }
    data.setdefault(name, {"versions": [], "production_version": None})
    data[name]["versions"].append(entry)
    _save(data)
    return entry


def promote_to_production(name: str, version: str) -> bool:
    data = _load()
    if name not in data:
        return False
    versions = {v["version"]: v for v in data[name]["versions"]}
    if version not in versions:
        return False
    for v in data[name]["versions"]:
        v["status"] = "archived" if v["version"] != version else "production"
    data[name]["production_version"] = version
    _save(data)
    return True


def rollback(name: str) -> str | None:
    """Roll back to the previous production version, if one exists."""
    data = _load()
    if name not in data:
        return None
    prod_versions = [v for v in data[name]["versions"] if v["status"] in ("production", "archived")]
    prod_versions.sort(key=lambda v: v["created_at"])
    archived = [v for v in prod_versions if v["status"] == "archived"]
    if not archived:
        return None
    target = archived[-1]
    promote_to_production(name, target["version"])
    return target["version"]


def get_production_model(name: str) -> dict | None:
    data = _load()
    entry = data.get(name)
    if not entry or not entry.get("production_version"):
        return None
    for v in entry["versions"]:
        if v["version"] == entry["production_version"]:
            return v
    return None


def list_versions(name: str) -> list[dict]:
    return _load().get(name, {}).get("versions", [])
