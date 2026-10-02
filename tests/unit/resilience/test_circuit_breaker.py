import pytest
from packages.resilience.circuit_breaker import CircuitBreaker, CircuitOpenError


def test_circuit_opens_after_threshold_failures():
    breaker = CircuitBreaker(failure_threshold=2, reset_seconds=60)

    def always_fails():
        raise ValueError("boom")

    for _ in range(2):
        with pytest.raises(ValueError):
            breaker.call(always_fails)

    with pytest.raises(CircuitOpenError):
        breaker.call(always_fails)


def test_circuit_resets_failure_count_on_success():
    breaker = CircuitBreaker(failure_threshold=2, reset_seconds=60)
    calls = {"n": 0}

    def flaky():
        calls["n"] += 1
        if calls["n"] == 1:
            raise ValueError("boom")
        return "ok"

    with pytest.raises(ValueError):
        breaker.call(flaky)
    assert breaker.call(flaky) == "ok"
    assert breaker.failure_count == 0
