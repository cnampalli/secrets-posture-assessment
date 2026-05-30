import questionnaire.roadmap_generator as rg


def test_seed_risk_mapping():
    assert rg.seed_risk("P0") == "High"
    assert rg.seed_risk("P1") == "Med"
    assert rg.seed_risk("P2") == "Low"
    assert rg.seed_risk("") == "Low"
    assert rg.seed_risk(None) == "Low"
    assert rg.seed_risk("weird") == "Low"


def test_quadrant_corners():
    assert rg.quadrant("High", "Low") == "Quick wins"
    assert rg.quadrant("High", "High") == "Major projects"
    assert rg.quadrant("Low", "Low") == "Fill-ins"
    assert rg.quadrant("Low", "High") == "Hard slogs"


def test_quadrant_med_bands():
    # Med risk counts as the high side; Med effort counts as the low (actionable) side.
    assert rg.quadrant("Med", "Med") == "Quick wins"
    assert rg.quadrant("Med", "High") == "Major projects"
    assert rg.quadrant("Low", "Med") == "Fill-ins"
