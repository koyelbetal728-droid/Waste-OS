# ADR 004: Local-first AI

**Decision:** Prefer Ollama (local LLM) and a small scikit-learn classifier
over mandatory paid APIs, so the platform works without external API keys.
**Trade-off:** The bundled classifier (packages/ml/classification) is
intentionally simple — a real CNN would need GPU training infrastructure
this scaffold doesn't assume you have.
