from packages.special_waste.food.donation import donation_eligibility


def test_spoiled_food_never_eligible():
    result = donation_eligibility("spoiled", 1)
    assert result["eligible_for_donation"] is False


def test_fresh_within_window_is_eligible():
    result = donation_eligibility("fresh", 2)
    assert result["eligible_for_donation"] is True


def test_fresh_but_past_holding_window_is_not_eligible():
    result = donation_eligibility("fresh", 6)
    assert result["eligible_for_donation"] is False
