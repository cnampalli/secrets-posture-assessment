"""WS1 validator-side tests: documented IGA tokens, the descriptor-declared
vendor-fit exception (+ fit-grid citation gate), and the cross-domain
zero-violation gate.

All three domains must validate clean; this is the recurring debt gate.
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "matrix"))
import pytest

import validate_data as vd
from domains import DOMAINS


# ---------------------------------------------------------------- item 1: roles

def test_informative_and_threat_context_are_valid_roles():
    rows = [{"framework_role": "INFORMATIVE"},
            {"framework_role": "THREAT-CONTEXT"},
            {"framework_role": "PRIMARY-LENS"},
            {"framework_role": "BACK-MAP"},
            {"framework_role": "ADVERSARY-LENS"}]
    assert vd.check_enum("regulatory-trace.csv", rows, "framework_role", vd.VALID_ROLES) == []


def test_bogus_role_still_rejected():
    # anti-fabrication gate must not be weakened: unknown roles still fail
    rows = [{"framework_role": "MADE-UP-ROLE"}]
    errs = vd.check_enum("regulatory-trace.csv", rows, "framework_role", vd.VALID_ROLES)
    assert errs == ["regulatory-trace.csv: invalid framework_role 'MADE-UP-ROLE'"]


def test_evidence_compliance_roles_unchanged():
    # new roles must remain EXCLUDED from evidence-pack binding
    assert vd.EVIDENCE_COMPLIANCE_ROLES == {"PRIMARY-LENS", "BACK-MAP"}


@pytest.mark.parametrize("role", ["INFORMATIVE", "THREAT-CONTEXT", "ADVERSARY-LENS"])
def test_non_compliance_roles_skipped_by_evidence_binding(role):
    # a dangling evidence ref on a non-compliance row must NOT be collected
    trace = [{"framework_role": role, "control_code": "X-1",
              "evidence_item_ids": "EV-DOES-NOT-EXIST"}]
    assert vd.check_evidence_packs(trace, []) == []


def test_compliance_role_evidence_binding_still_enforced():
    trace = [{"framework_role": "PRIMARY-LENS", "control_code": "X-1",
              "evidence_item_ids": "EV-DOES-NOT-EXIST"}]
    errs = vd.check_evidence_packs(trace, [])
    assert any("EV-DOES-NOT-EXIST" in e for e in errs)


# ------------------------------------------------------------ item 2: dimension

def test_scope_is_valid_evidence_dimension():
    catalog = [{"ev_id": "EV-1", "dimension": "scope", "tier": "primary",
                "citation_keys": "k1"}]
    assert vd.check_evidence_packs([], catalog) == []


def test_bogus_dimension_still_rejected():
    catalog = [{"ev_id": "EV-1", "dimension": "vibes", "tier": "primary",
                "citation_keys": "k1"}]
    errs = vd.check_evidence_packs([], catalog)
    assert errs == ["evidence-catalog.csv: invalid dimension 'vibes' (item EV-1)"]


# ------------- item 3: descriptor-declared vendor-fit (matrix-less exception)
# "Matrix-less" is declared in the domain descriptor (`vendor_fit:` key), NOT
# inferred from a *-vendor-fit.csv filename glob — a stray supplemental fit file
# in a matrix-using domain must never disable that domain's empty-matrix guard.

def test_domain_dataclass_carries_vendor_fit():
    assert DOMAINS["iga"].vendor_fit == "iga-vendor-fit.csv"
    assert DOMAINS["secrets"].vendor_fit is None
    assert DOMAINS["pam"].vendor_fit is None


def test_resolve_descriptor_for_iga_data_dir():
    d = vd.resolve_domain_descriptor(str(ROOT), str(ROOT / "matrix" / "domains" / "iga"))
    assert d is not None and d["slug"] == "iga"
    assert d["vendor_fit"] == "iga-vendor-fit.csv"


def test_resolve_descriptor_for_secrets_data_dir_declares_no_vendor_fit():
    # secrets' data_dir is matrix/domains/secrets and it keeps its vendor matrix
    d = vd.resolve_domain_descriptor(str(ROOT), str(ROOT / "matrix" / "domains" / "secrets"))
    assert d is not None and d["slug"] == "secrets"
    assert not d.get("vendor_fit")


def test_stray_fit_file_does_not_make_a_dir_matrixless(tmp_path):
    # regression for the glob heuristic: a stray pam-vendor-fit.csv in an
    # unregistered dir resolves to NO descriptor -> the empty-matrix guard holds
    (tmp_path / "pam-vendor-fit.csv").write_text("area,vendor,fit\n", encoding="utf-8")
    assert vd.resolve_domain_descriptor(str(ROOT), str(tmp_path)) is None


def test_header_only_vendor_caps_ok_when_descriptor_declares_vendor_fit():
    assert vd.check_aggregate_vendor_capabilities([], vendor_fit="iga-vendor-fit.csv") == []


def test_header_only_vendor_caps_fails_without_declared_vendor_fit():
    # secrets/PAM declare no vendor_fit -> empty vendor matrix stays a violation
    errs = vd.check_aggregate_vendor_capabilities([], vendor_fit=None)
    assert errs == ["vendor-capabilities.csv: empty (no data rows)"]


def test_nonempty_vendor_caps_still_validated_when_vendor_fit_declared():
    # the exception is for header-only files ONLY; real rows are still checked
    bad = dict({c: "x" for c in vd.VENDOR_REQUIRED}, maturity="9", coverage="")
    errs = vd.check_aggregate_vendor_capabilities([bad], vendor_fit="iga-vendor-fit.csv")
    assert any("maturity '9'" in e for e in errs)
    assert any("empty coverage" in e for e in errs)


# --------------------- item 3b: the declared fit grid is itself citation-gated
# The fit file substitutes for the vendor matrix, so its NATIVE/PARTIAL/ADD-ON
# claims must clear the same anti-fabrication bar: every row sourced.

FIT_NAME = "iga-vendor-fit.csv"
FIT_HEADER = ",".join(vd.VENDOR_FIT_REQUIRED) + "\n"
GOOD_FIT_ROW = ("SailPoint,sailpoint-isc,JML,NATIVE,Lifecycle states drive access,"
                "https://docs.example/lifecycle,sailpoint-isc-lifecycle,"
                "Lifecycle states describe a user's status in the organization\n")


def _fit_errs(tmp_path, text):
    (tmp_path / FIT_NAME).write_text(text, encoding="utf-8")
    return vd.check_vendor_fit(str(tmp_path), FIT_NAME)


def test_vendor_fit_good_row_passes(tmp_path):
    assert _fit_errs(tmp_path, FIT_HEADER + GOOD_FIT_ROW) == []


@pytest.mark.parametrize("grade", sorted(vd.VALID_FIT_GRADES))
def test_vendor_fit_all_grades_accepted(tmp_path, grade):
    assert vd.VALID_FIT_GRADES == {"NATIVE", "PARTIAL", "ADD-ON"}
    assert _fit_errs(tmp_path, FIT_HEADER + GOOD_FIT_ROW.replace("NATIVE", grade)) == []


def test_vendor_fit_missing_file_is_violation(tmp_path):
    # descriptor declares the fit grid but it does not exist -> no vendor evidence
    errs = vd.check_vendor_fit(str(tmp_path), FIT_NAME)
    assert len(errs) == 1 and FIT_NAME in errs[0] and "missing" in errs[0]


def test_vendor_fit_header_only_is_violation(tmp_path):
    # header-only fit grid + header-only matrix == NO vendor evidence at all
    assert _fit_errs(tmp_path, FIT_HEADER) == [f"{FIT_NAME}: empty (no data rows)"]


def test_vendor_fit_missing_required_column_rejected(tmp_path):
    errs = _fit_errs(tmp_path, "vendor,fit\nSailPoint,NATIVE\n")
    assert any("missing required column" in e for e in errs)


def test_vendor_fit_bad_grade_rejected(tmp_path):
    errs = _fit_errs(tmp_path, FIT_HEADER + GOOD_FIT_ROW.replace("NATIVE", "TOTALLY-NATIVE"))
    assert errs and "TOTALLY-NATIVE" in errs[0]


def test_vendor_fit_empty_grade_rejected(tmp_path):
    errs = _fit_errs(tmp_path, FIT_HEADER + GOOD_FIT_ROW.replace("NATIVE", ""))
    assert errs and "invalid fit" in errs[0]


@pytest.mark.parametrize("col", ["justification", "evidence_url", "citation_keys",
                                 "evidence_quote"])
def test_vendor_fit_unsourced_claim_rejected(tmp_path, col):
    # anti-fabrication: a fit claim without a source is a violation
    row = {"vendor": "SailPoint", "vendor_slug": "sailpoint-isc", "area": "JML",
           "fit": "NATIVE", "justification": "j", "evidence_url": "u",
           "citation_keys": "k", "evidence_quote": "q"}
    row[col] = ""
    text = FIT_HEADER + ",".join(row[c] for c in vd.VENDOR_FIT_REQUIRED) + "\n"
    errs = _fit_errs(tmp_path, text)
    assert len(errs) == 1 and col in errs[0]


def test_real_iga_fit_grid_passes_the_gate():
    # 16 rows, all NATIVE/PARTIAL, fully sourced — must clear the new gate as-is
    assert vd.check_vendor_fit(str(ROOT / "matrix" / "domains" / "iga"), FIT_NAME) == []


# -------------------------------------------------- item 4: cross-domain gate
# Parametrized off the domain registry: a 4th domain YAML auto-joins the gate.

@pytest.mark.parametrize("slug", sorted(DOMAINS))
def test_domain_has_zero_violations(slug):
    violations = vd.validate_all(root=str(ROOT), data_dir=DOMAINS[slug].data_dir)
    assert violations == [], f"{slug}: {len(violations)} violation(s):\n" + "\n".join(violations)


# ------------------------------------------------------- main() exit contract
# W0.1 (2026-07-02): the no-arg CLI validates EVERY registered domain; the
# historical secrets-only default let PAM/IGA defects pass a "clean" run.

def test_main_exits_nonzero_on_violations(monkeypatch, capsys):
    # single-domain narrowing contract unchanged when --data-dir is explicit
    monkeypatch.setattr(vd, "validate_all", lambda root, data_dir=None: ["fake: violation"])
    assert vd.main(["--data-dir", "matrix/domains/secrets"]) == 1
    out = capsys.readouterr().out
    assert "fake: violation" in out and "1 violation(s) found" in out


def test_main_exits_zero_when_clean(monkeypatch, capsys):
    monkeypatch.setattr(vd, "validate_all", lambda root, data_dir=None: [])
    assert vd.main(["--root", str(ROOT)]) == 0
    assert "All CSV data contracts valid" in capsys.readouterr().out


def test_default_cli_run_covers_every_registered_domain(monkeypatch):
    seen = []
    monkeypatch.setattr(vd, "validate_all",
                        lambda root, data_dir=None: (seen.append(data_dir), [])[1])
    assert vd.main(["--root", str(ROOT)]) == 0
    import os
    names = {os.path.basename(os.path.realpath(d)) for d in seen}
    assert names == set(DOMAINS), f"default run visited {names}, expected {set(DOMAINS)}"


def test_violation_in_non_secrets_domain_fails_default_run(monkeypatch, capsys):
    # the exact failure mode of the old default: a PAM-only defect must now
    # fail the bare CLI run, slug-prefixed, without stopping the other domains
    def fake(root, data_dir=None):
        return ["use-cases.csv: seeded defect"] if data_dir.rstrip("/").endswith("pam") else []
    monkeypatch.setattr(vd, "validate_all", fake)
    assert vd.main(["--root", str(ROOT)]) == 1
    out = capsys.readouterr().out
    assert "[pam] use-cases.csv: seeded defect" in out and "1 violation(s) found" in out


def test_iter_domain_data_dirs_registry_driven():
    got = dict(vd.iter_domain_data_dirs(str(ROOT)))
    assert set(got) == {"secrets", "pam", "iga"}
    for slug, d in got.items():
        import os
        assert os.path.isdir(d), f"{slug}: data dir {d} does not exist"


# ------------------------------------------ regression pins for closed defects
# REG-F1 / IGA-F1 / PAM-SME-01 (closed 2026-06 in commits 0d3ddfe/5ca36c6):
# pin the closed state so the defect classes are unrevivable without a red test.

def _rows(path):
    import csv
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_pam_cps234_s22_maps_third_party_ucs_only():
    # REG-F1: §22 is the THIRD-PARTY control-evaluation obligation; binding it to
    # internal PAM UCs was the right-ID-wrong-scope fabrication class
    trace = _rows(str(ROOT / "matrix" / "domains" / "pam" / "regulatory-trace.csv"))
    for r in trace:
        if r["control_code"] == "CPS234-§22":
            ucs = {u.strip() for u in r["uc_ids"].split(";") if u.strip()}
            assert ucs == {"UC-P-011"}, f"CPS234-§22 mapped to {sorted(ucs)} — third-party scope only"


def test_iga_has_no_cps234_s22_residue():
    # IGA-F1: the §22→§21 remap must hold in BOTH the trace and use-cases backmaps
    for fn in ("regulatory-trace.csv", "use-cases.csv"):
        text = (ROOT / "matrix" / "domains" / "iga" / fn).read_text(encoding="utf-8")
        assert "§22" not in text, f"iga/{fn}: CPS234-§22 residue"


def test_ucp019_backmap_is_ism_1405_not_1304():
    # PAM-SME-01: UC-P-019's stale ISM-1304 self-declaration contradicted its trace
    ucs = _rows(str(ROOT / "matrix" / "domains" / "pam" / "use-cases.csv"))
    row = next(r for r in ucs if r["uc_id"] == "UC-P-019")
    codes = {c.strip() for c in row["backmap_codes"].split(";")}
    assert "ISM-1405" in codes and "ISM-1304" not in codes, f"UC-P-019 backmaps: {sorted(codes)}"


# ---------------------------------------------- NEW-01: control-scope gate
# The 2026-07-02 review proved the backmap↔trace gate is blind to a SYMMETRIC
# right-ID-wrong-scope defect (the original REG-F1 shape). check_control_scope
# closes that class: relationship-scoped controls only bind UCs whose own text
# evidences the relationship.

SCOPE_CFG = {"scope_restrictions": {"third-party": {
    "controls": ["CPS234-§22"], "keyword_any": ["vendor", "third-party"]}}}


def test_control_scope_catches_internal_uc_on_third_party_control():
    # the original REG-F1, reproduced symmetrically: internal UC + §22 in the trace
    ucs = [{"uc_id": "UC-P-019", "short_title": "Agent privileged-session brokering",
            "story": "autonomous agents obtain privileged sessions through the broker",
            "acceptance_criteria": "sessions recorded"}]
    trace = [{"control_code": "CPS234-§22", "uc_ids": "UC-P-019"}]
    errs = vd.check_control_scope(ucs, trace, SCOPE_CFG)
    assert len(errs) == 1 and "right-ID-wrong-scope" in errs[0] and "UC-P-019" in errs[0]


def test_control_scope_passes_evidenced_third_party_uc():
    ucs = [{"uc_id": "UC-P-011", "short_title": "Privileged remote / third-party vendor access",
            "story": "vendor engineers access via brokered sessions", "acceptance_criteria": "x"}]
    trace = [{"control_code": "CPS234-§22", "uc_ids": "UC-P-011"}]
    assert vd.check_control_scope(ucs, trace, SCOPE_CFG) == []


def test_control_scope_fails_closed_without_registry():
    errs = vd.check_control_scope([], [], {})
    assert len(errs) == 1 and "scope_restrictions" in errs[0]


def test_control_scope_fails_closed_on_empty_scope_spec():
    errs = vd.check_control_scope([], [], {"scope_restrictions": {"third-party": {}}})
    assert len(errs) == 1 and "fail-closed" in errs[0]


def test_control_scope_real_data_clean_all_domains():
    import os
    sem = vd.load_yaml(str(ROOT / "matrix" / "config" / "control-semantics.yaml"))
    for slug in sorted(DOMAINS):
        base = os.path.join(str(ROOT), "matrix", "domains", slug)
        ucs = vd.load_csv(os.path.join(base, "use-cases.csv"))
        trace = vd.load_csv(os.path.join(base, "regulatory-trace.csv"))
        assert vd.check_control_scope(ucs, trace, sem) == [], slug


def test_backmap_gate_catches_stale_control_scope():
    # the structural gate itself: a UC self-declaring a control whose trace row
    # doesn't list it must fail (right-ID-wrong-scope / stale-mapping class)
    ucs = [{"uc_id": "UC-P-019", "backmap_codes": "ISM-1304"}]
    trace = [{"control_code": "ISM-1405", "uc_ids": "UC-P-019"}]
    errs = vd.check_backmap_trace_consistency(ucs, trace)
    assert len(errs) == 1 and "ISM-1304" in errs[0]


def test_iga_agentic_ucs_have_archetypes():
    import csv, os
    base = os.path.join(ROOT, "matrix", "domains", "iga")
    ucs = {r["uc_id"] for r in csv.DictReader(open(os.path.join(base, "use-cases.csv"), encoding="utf-8"))}
    mapped = {r["uc_id"] for r in csv.DictReader(open(os.path.join(base, "uc-archetype-map.csv"), encoding="utf-8"))}
    for uc in ("UC-I-017", "UC-I-018", "UC-I-019"):
        assert uc in ucs and uc in mapped, f"{uc} missing UC row or archetype mapping"


def test_secrets_agentic_ucs_present():
    import csv, os
    base = os.path.join(ROOT, "matrix", "domains", "secrets")
    ucs = {r["uc_id"] for r in csv.DictReader(open(os.path.join(base, "use-cases.csv"), encoding="utf-8"))}
    for uc in ("UC-F-028", "UC-F-029", "UC-F-030"):
        assert uc in ucs, f"{uc} missing from secrets use-cases.csv"


def test_informative_frameworks_not_leaked_into_compliance():
    # OC-01 regression guard: any framework marked "(informative)" in frameworks.yaml that a
    # domain actually maps in its regulatory-trace MUST be in that domain's informative_frameworks
    # (so it is excluded from the buyer-facing compliance %). Prevents per-domain config drift.
    import os, csv, yaml
    from domains import DOMAINS
    fw = yaml.safe_load(open(os.path.join(ROOT, "matrix", "config", "frameworks.yaml"), encoding="utf-8"))
    informative = {slug for slug, meta in fw.items()
                   if isinstance(meta, dict) and "(informative)" in (meta.get("subtitle") or "")}
    assert informative, "expected at least one (informative)-marked framework"
    for slug in ("secrets", "pam", "iga"):
        used = {r["framework_slug"] for r in csv.DictReader(
            open(os.path.join(ROOT, "matrix", "domains", slug, "regulatory-trace.csv"), encoding="utf-8"))}
        leaked = (informative & used) - set(DOMAINS[slug].informative_frameworks)
        assert not leaked, f"{slug}: informative frameworks leak into compliance %: {sorted(leaked)}"


def test_npe_conformance_values_in_legend():
    # IAM-01 regression guard: every npe_conformance value across all domains must be in
    # the closed legend (no off-legend "NPE"), so cross-domain conformance claims hold.
    import csv, os
    legend = {"CONFORMANT", "HUMAN-IDENTITY", "CREDENTIAL-NOT-IDENTITY",
              "CROSS-CUTTING-ATTRIBUTE", "HUMAN-USE-ANTIPATTERN"}
    for dom in ("secrets", "pam", "iga"):
        path = os.path.join(ROOT, "matrix", "domains", dom, "identity-catalog.csv")
        for r in csv.DictReader(open(path, encoding="utf-8")):
            assert r["npe_conformance"] in legend, \
                f"{dom} {r['nhi_id']}: off-legend npe_conformance '{r['npe_conformance']}'"


def test_validator_rejects_off_legend_npe_conformance():
    # the gate itself must catch a bad value (not just the data being clean today)
    import sys, os
    sys.path.insert(0, os.path.join(ROOT, "matrix"))
    import validate_data as vd
    bad = [{"nhi_id": "X-1", "npe_conformance": "NPE"}]
    errs = vd.check_enum("identity-catalog.csv", bad, "npe_conformance", vd.VALID_NPE_CONFORMANCE)
    assert len(errs) == 1 and "npe_conformance" in errs[0]


def test_pam_agentic_ucs_and_identity_present():
    import csv, os
    base = os.path.join(ROOT, "matrix", "domains", "pam")
    ucs = {r["uc_id"] for r in csv.DictReader(open(os.path.join(base, "use-cases.csv"), encoding="utf-8"))}
    mapped = {r["uc_id"] for r in csv.DictReader(open(os.path.join(base, "uc-archetype-map.csv"), encoding="utf-8"))}
    ids = {r["nhi_id"] for r in csv.DictReader(open(os.path.join(base, "identity-catalog.csv"), encoding="utf-8"))}
    for uc in ("UC-P-019", "UC-P-020", "UC-P-021"):
        assert uc in ucs and uc in mapped, f"{uc} missing UC row or archetype mapping"
    assert "PID-021" in ids, "PID-021 missing from PAM identity-catalog"
