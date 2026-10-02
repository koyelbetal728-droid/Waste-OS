from packages.waste.hazard import screen_hazard


def test_no_category_is_unknown():
    assert screen_hazard(None, 0.9) == "unknown"


def test_hazard_keyword_high_confidence_is_hazardous():
    assert screen_hazard("Lithium battery", 0.9) == "hazardous"


def test_hazard_keyword_low_confidence_is_potentially_hazardous():
    assert screen_hazard("Battery pack", 0.5) == "potentially_hazardous"


def test_non_hazard_category_is_none_detected():
    assert screen_hazard("Cardboard box", 0.9) == "none_detected"
