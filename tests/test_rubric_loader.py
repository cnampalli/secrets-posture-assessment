import pathlib, re
import pytest
import questionnaire.rubric_loader as rl

ROOT = pathlib.Path(__file__).resolve().parents[1]
METH = ROOT / "methodology"
UCS = rl.load_rubric(METH)
BY_ID = {u["uc_id"]: u for u in UCS}


def test_all_47_use_cases_resolve():
    assert len(UCS) == 47


def test_category_from_prefix():
    assert BY_ID["UC-F-001"]["category"] == "Functional"
    assert BY_ID["UC-N-002"]["category"] == "Non-functional"


def test_title_from_notes():
    assert BY_ID["UC-F-001"]["title"] == "Prevent plaintext secrets in repos"


def test_ladder_uc_fills_params():
    uc = BY_ID["UC-F-001"]
    assert uc["kind"] == "ladder"
    assert uc["archetype"] == "A1"
    q1 = uc["questions"][0]
    assert q1["qid"] == "A1-Q1"
    assert q1["informs_state"] == "GAP_PARTIAL"
    assert q1["text"] == "Is secret push-protection deployed at all relevant gates for repo-committed secrets?"


def test_no_leftover_slots_anywhere():
    for uc in UCS:
        if uc["kind"] == "ladder":
            for q in uc["questions"]:
                assert "{" not in q["text"], f"{uc['uc_id']} {q['qid']} unfilled: {q['text']}"


def test_a0_use_cases_are_bespoke():
    uc = BY_ID["UC-F-017"]
    assert uc["kind"] == "bespoke"
    assert uc["archetype"] == "A0"
    assert len(uc["sub_criteria"]) == 3
    sc = uc["sub_criteria"][0]
    assert sc["sub_id"] == "UC-F-017.1"
    assert "TEE attestation" in sc["question"]


def test_missing_param_raises(tmp_path):
    aq = tmp_path / "archetype-questions.csv"
    aq.write_text("archetype_id,q_id,question_template,dimension,informs_state\n"
                  'AX,AX-Q1,"Is {control} on?",coverage,GAP_PARTIAL\n', encoding="utf-8")
    arch = tmp_path / "assessment-archetypes.csv"
    arch.write_text("archetype_id,name,intent,met_def,partial_def,gap_def,na_def,evidence_expectation\n"
                    "AX,Test,i,m,p,g,n,e\n", encoding="utf-8")
    mp = tmp_path / "uc-archetype-map.csv"
    mp.write_text("uc_id,archetype_id,params,notes\nUC-F-900,AX,nope=1,Title\n", encoding="utf-8")
    bs = tmp_path / "bespoke-criteria.csv"
    bs.write_text("uc_id,sub_id,sub_criterion,question,evidence\n", encoding="utf-8")
    with pytest.raises(rl.RubricError):
        rl.load_rubric(tmp_path)
