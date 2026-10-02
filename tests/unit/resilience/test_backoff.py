from packages.resilience.backoff import compute_delay


def test_delay_increases_with_attempt():
    assert compute_delay(1) > compute_delay(0)


def test_delay_is_capped():
    assert compute_delay(20, max_seconds=30.0) == 30.0
