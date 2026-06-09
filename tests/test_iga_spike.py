import pathlib
import questionnaire.rubric_loader as rl

ROOT = pathlib.Path(__file__).resolve().parents[1]
METH = ROOT / "methodology"
SPIKE = ROOT / "spikes" / "iga"

UCS = rl.load_rubric(METH, data_dir=SPIKE)
BY_ID = {u["uc_id"]: u for u in UCS}


def test_all_11_iga_use_cases_resolve():
    assert {u["uc_id"] for u in UCS} == {f"UC-I-{i:03d}" for i in range(1, 12)}


def test_every_iga_uc_is_a_ladder_with_questions():
    for uc in UCS:
        assert uc["kind"] == "ladder", f"{uc['uc_id']} is not a ladder"
        assert uc["questions"], f"{uc['uc_id']} has no questions"


def test_no_unfilled_slots_in_iga_questions():
    for uc in UCS:
        for q in uc["questions"]:
            assert "{" not in q["text"], f"{uc['uc_id']} {q['qid']} unfilled: {q['text']}"


def test_archetype_spread_exercises_the_governance_library():
    used = {u["archetype"] for u in UCS}
    assert {"A1", "A2", "A3", "A5", "A7", "A8"} <= used


def test_category_mapping():
    assert BY_ID["UC-I-008"]["category"] == "Non-functional"
    assert BY_ID["UC-I-001"]["category"] == "Functional"
