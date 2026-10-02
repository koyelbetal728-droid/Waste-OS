from packages.ai.orchestrator.ui_intents import classify_intent


def test_waste_stats_intent():
    assert classify_intent("how much waste do I have") == "waste_stats"


def test_recycling_rate_intent():
    assert classify_intent("what's my recycling rate") == "recycling_rate"


def test_schedule_pickup_intent():
    assert classify_intent("schedule a pickup for tomorrow") == "schedule_pickup"


def test_hotspots_intent():
    assert classify_intent("show me hotspots near me") == "hotspots"


def test_rewards_intent():
    assert classify_intent("how many green points do I have") == "rewards"


def test_marketplace_intent():
    assert classify_intent("show marketplace listings") == "marketplace"


def test_unmatched_message_is_unknown():
    assert classify_intent("random gibberish xyz") == "unknown"
