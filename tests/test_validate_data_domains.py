"""WS1 validator-side tests: documented IGA tokens + matrix-less vendor exception,
plus the cross-domain zero-violation gate.

NOTE: the IGA gate case is EXPECTED RED until the parallel data-fix agent's output
is integrated — it is the WS1 exit gate. Do not skip/xfail it.
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "matrix"))
import pytest

import validate_data as vd


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


# --------------------------- item 3: header-only vendor-capabilities (matrix-less)

def _write(p, text):
    p.write_text(text, encoding="utf-8")


def test_header_only_vendor_caps_ok_with_vendor_fit_sibling(tmp_path):
    _write(tmp_path / "iga-vendor-fit.csv", "area,vendor,fit\n")
    _write(tmp_path / "vendor-capabilities.csv", ",".join(vd.VENDOR_REQUIRED) + "\n")
    rows = vd.load_csv(str(tmp_path / "vendor-capabilities.csv"))
    assert rows == []
    assert vd.check_aggregate_vendor_capabilities(str(tmp_path), rows) == []


def test_header_only_vendor_caps_fails_without_vendor_fit_sibling(tmp_path):
    # secrets/PAM have no *-vendor-fit.csv -> empty vendor matrix stays a violation
    _write(tmp_path / "vendor-capabilities.csv", ",".join(vd.VENDOR_REQUIRED) + "\n")
    rows = vd.load_csv(str(tmp_path / "vendor-capabilities.csv"))
    errs = vd.check_aggregate_vendor_capabilities(str(tmp_path), rows)
    assert errs == ["vendor-capabilities.csv: empty (no data rows)"]


def test_nonempty_vendor_caps_still_validated_in_matrixless_domain(tmp_path):
    # the exception is for header-only files ONLY; real rows are still checked
    _write(tmp_path / "iga-vendor-fit.csv", "area,vendor,fit\n")
    bad = dict({c: "x" for c in vd.VENDOR_REQUIRED}, maturity="9", coverage="")
    errs = vd.check_aggregate_vendor_capabilities(str(tmp_path), [bad])
    assert any("maturity '9'" in e for e in errs)
    assert any("empty coverage" in e for e in errs)


def test_is_matrixless_domain_detection(tmp_path):
    assert vd.is_matrixless_domain(str(tmp_path)) is False
    _write(tmp_path / "iga-vendor-fit.csv", "area,vendor,fit\n")
    assert vd.is_matrixless_domain(str(tmp_path)) is True


# -------------------------------------------------- item 4: cross-domain gate

DOMAIN_DATA_DIRS = {
    "secrets": None,                                       # default <root>/matrix
    "pam": str(ROOT / "matrix" / "domains" / "pam"),
    "iga": str(ROOT / "matrix" / "domains" / "iga"),       # EXPECTED RED until data-debt fixed (WS1 exit gate)
}


@pytest.mark.parametrize("domain", sorted(DOMAIN_DATA_DIRS))
def test_domain_has_zero_violations(domain):
    violations = vd.validate_all(root=str(ROOT), data_dir=DOMAIN_DATA_DIRS[domain])
    assert violations == [], f"{domain}: {len(violations)} violation(s):\n" + "\n".join(violations)


# ------------------------------------------------------- main() exit contract

def test_main_exits_nonzero_on_violations(monkeypatch, capsys):
    monkeypatch.setattr(vd, "validate_all", lambda root, data_dir=None: ["fake: violation"])
    assert vd.main([]) == 1
    out = capsys.readouterr().out
    assert "fake: violation" in out and "1 violation(s) found" in out


def test_main_exits_zero_when_clean(monkeypatch, capsys):
    monkeypatch.setattr(vd, "validate_all", lambda root, data_dir=None: [])
    assert vd.main([]) == 0
    assert "All CSV data contracts valid" in capsys.readouterr().out
