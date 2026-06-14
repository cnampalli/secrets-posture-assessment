import pathlib, re
import pytest
import questionnaire.rubric_loader as rl

ROOT = pathlib.Path(__file__).resolve().parents[1]
METH = ROOT / "methodology"
UCS = rl.load_rubric(METH)
BY_ID = {u["uc_id"]: u for u in UCS}


def test_all_50_use_cases_resolve():
    assert len(UCS) == 50  # M3.2: +3 agent-credential UCs (UC-F-028/029/030)


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


def test_archetype_with_no_questions_raises(tmp_path):
    # a non-A0 UC mapped to an archetype that has no questions must fail loudly,
    # not silently produce an empty (auto-MET) question set.
    aq = tmp_path / "archetype-questions.csv"
    aq.write_text("archetype_id,q_id,question_template,dimension,informs_state\n", encoding="utf-8")
    arch = tmp_path / "assessment-archetypes.csv"
    arch.write_text("archetype_id,name,intent,met_def,partial_def,gap_def,na_def,evidence_expectation\n"
                    "BX,Empty,i,m,p,g,n,e\n", encoding="utf-8")
    mp = tmp_path / "uc-archetype-map.csv"
    mp.write_text("uc_id,archetype_id,params,notes\nUC-F-901,BX,,Title\n", encoding="utf-8")
    bs = tmp_path / "bespoke-criteria.csv"
    bs.write_text("uc_id,sub_id,sub_criterion,question,evidence\n", encoding="utf-8")
    with pytest.raises(rl.RubricError):
        rl.load_rubric(tmp_path)


# --- domain-aware loading + regulatory evidence binding --------------------

PAM = ROOT / "matrix" / "domains" / "pam"
PAM_UCS = rl.load_rubric(METH, data_dir=PAM)
PAM_BY_ID = {u["uc_id"]: u for u in PAM_UCS}


def _ev_on(uc, dimension):
    """All evidence ev_ids bound to questions of a given dimension on a UC."""
    out = []
    for q in uc.get("questions", []):
        if q["dimension"] == dimension:
            out += [e["ev_id"] for e in q.get("evidence", [])]
    return out


def test_pam_loads_all_18_use_cases():
    # the PAM questionnaire must reach parity with the PAM matrix report (all 18 UCs),
    # not the original 3-UC demo slice.
    assert {u["uc_id"] for u in PAM_UCS} == {f"UC-P-{i:03d}" for i in range(1, 19)}


def test_pam_all_use_cases_are_ladder():
    # every PAM UC maps to a reusable archetype (no bespoke A0 long-tail in this domain).
    for uc in PAM_UCS:
        assert uc["kind"] == "ladder", f"{uc['uc_id']} is not a ladder UC"
        assert uc["questions"], f"{uc['uc_id']} has no questions"


def test_pam_archetypes_assigned():
    assert PAM_BY_ID["UC-P-001"]["archetype"] == "A4"
    assert PAM_BY_ID["UC-P-002"]["archetype"] == "A1"
    assert PAM_BY_ID["UC-P-003"]["archetype"] == "A3"
    # spot-check a sample of the newly-mapped tail
    assert PAM_BY_ID["UC-P-007"]["archetype"] == "A1"   # MFA -> preventive guardrail
    assert PAM_BY_ID["UC-P-014"]["archetype"] == "A5"   # recertification -> inventory & attestation
    assert PAM_BY_ID["UC-P-017"]["archetype"] == "A8"   # resilience -> periodic assurance artifact


def test_pam_questions_have_no_leftover_slots():
    for uc in PAM_UCS:
        for q in uc["questions"]:
            assert "{" not in q["text"], f"{uc['uc_id']} {q['qid']}: {q['text']}"


def test_primary_evidence_binds_to_coverage_question():
    # ISM-1304's credential-elimination register (coverage/primary) reaches UC-P-001
    cov = _ev_on(PAM_BY_ID["UC-P-001"], "coverage")
    assert "EV-PAM-CRED-ELIM-REGISTER" in cov
    item = next(e for q in PAM_BY_ID["UC-P-001"]["questions"]
                for e in q.get("evidence", []) if e["ev_id"] == "EV-PAM-CRED-ELIM-REGISTER")
    assert item["tier"] == "primary"
    assert item["requirement"]
    assert item["example_artifact"]  # non-authoritative hint carried through


def test_shared_item_is_deduped_and_reverse_mapped():
    # EV-PAM-VAULT-ROTATION-POLICY is referenced by BOTH ISM-1619 and CPS234-§21(b);
    # on UC-P-001 it must appear exactly once and list both controls it satisfies.
    uc = PAM_BY_ID["UC-P-001"]
    hits = [e for q in uc["questions"] for e in q.get("evidence", [])
            if e["ev_id"] == "EV-PAM-VAULT-ROTATION-POLICY"]
    assert len(hits) == 1, "shared item should be de-duplicated within the UC"
    assert set(hits[0]["satisfies"]) == {"ISM-1619", "CPS234-§21(b)"}


def test_evidence_shared_across_use_cases():
    # the credential-elimination register backs ISM-1304, which both UC-P-001 and
    # UC-P-002 map to -> the same artifact surfaces on both.
    assert "EV-PAM-CRED-ELIM-REGISTER" in _ev_on(PAM_BY_ID["UC-P-002"], "coverage")


def test_followup_tier_preserved_for_drilldown():
    flat = [e for q in PAM_BY_ID["UC-P-001"]["questions"] for e in q.get("evidence", [])]
    assert any(e["tier"] == "follow-up" for e in flat)
    assert any(e["tier"] == "primary" for e in flat)


def test_secrets_still_loads_without_evidence(tmp_path):
    # backward compatibility: methodology-only load is unchanged and carries no evidence
    secrets = rl.load_rubric(METH)
    assert len(secrets) == 50  # M3.2: +3 agent-credential UCs (UC-F-028/029/030)
    uc = next(u for u in secrets if u["uc_id"] == "UC-F-001")
    assert all(not q.get("evidence") for q in uc["questions"])


def test_unbound_evidence_falls_to_catch_all(tmp_path):
    # an evidence item whose dimension matches no question on the UC lands in
    # the per-UC "additional evidence" list, not dropped.
    (tmp_path / "archetype-questions.csv").write_text(
        "archetype_id,q_id,question_template,dimension,informs_state\n"
        'A1,A1-Q1,"Is {control} on for {nhi_population}?",coverage,GAP_PARTIAL\n', encoding="utf-8")
    (tmp_path / "assessment-archetypes.csv").write_text(
        "archetype_id,name,intent,met_def,partial_def,gap_def,na_def,evidence_expectation\n"
        "A1,Guardrail,i,m,p,g,n,e\n", encoding="utf-8")
    data = tmp_path / "data"; data.mkdir()
    (data / "uc-archetype-map.csv").write_text(
        "uc_id,archetype_id,params,notes\nUC-P-900,A1,control=x;nhi_population=y,T\n", encoding="utf-8")
    (data / "evidence-catalog.csv").write_text(
        "ev_id,requirement,dimension,tier,example_artifact,sensitivity_tag,citation_keys\n"
        "EV-X,req-cov,coverage,primary,,,c1\n"
        "EV-Y,req-cadence,cadence,follow-up,,,c1\n", encoding="utf-8")
    (data / "regulatory-trace.csv").write_text(
        "framework_slug,framework_role,control_code,uc_ids,evidence_item_ids\n"
        "asd-ism,BACK-MAP,ISM-1,UC-P-900,EV-X;EV-Y\n", encoding="utf-8")
    uc = rl.load_rubric(tmp_path, data_dir=data)[0]
    bound = [e["ev_id"] for q in uc["questions"] for e in q.get("evidence", [])]
    assert bound == ["EV-X"]                       # coverage item bound to the coverage question
    assert [e["ev_id"] for e in uc["evidence_additional"]] == ["EV-Y"]  # cadence has no question
