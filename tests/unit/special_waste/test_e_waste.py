from packages.special_waste.e_waste.classifier import determine_pathway


def test_working_device_is_reuse():
    assert determine_pathway("working") == "reuse"


def test_unknown_condition_defaults_to_recycle_conservatively():
    assert determine_pathway(None) == "recycle"


def test_non_functional_is_recycle():
    assert determine_pathway("non_functional") == "recycle"
