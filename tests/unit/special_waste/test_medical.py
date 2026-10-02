from packages.special_waste.medical.compliance import compliance_status


def test_sharps_requires_authorized_facility():
    result = compliance_status("sharps")
    assert result["requires_authorized_facility"] is True


def test_unknown_category_is_conservative():
    result = compliance_status(None)
    assert result["requires_authorized_facility"] is True
