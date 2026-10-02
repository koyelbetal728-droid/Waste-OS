"""Thin client for a local Ollama server. Degrades gracefully (never
fabricates a response) if Ollama isn't running — the orchestrator falls
back to a deterministic templated answer in that case. Wrapped in a real
circuit breaker so repeated Ollama outages don't waste a timeout on every
single request."""
import json
import urllib.request
import urllib.error
from packages.resilience.circuit_breaker import CircuitBreaker, CircuitOpenError

OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "llama3.2"

_breaker = CircuitBreaker(failure_threshold=3, reset_seconds=30.0)


def _do_generate(prompt: str, model: str, timeout: float) -> str | None:
    body = json.dumps({"model": model, "prompt": prompt, "stream": False}).encode()
    req = urllib.request.Request(OLLAMA_URL, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read())
        return data.get("response")


def generate(prompt: str, model: str = DEFAULT_MODEL, timeout: float = 8.0) -> str | None:
    try:
        return _breaker.call(_do_generate, prompt, model, timeout)
    except (urllib.error.URLError, TimeoutError, ConnectionError, CircuitOpenError):
        return None  # caller must fall back — never fabricate an LLM answer
