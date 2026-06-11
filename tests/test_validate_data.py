import csv
import pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "matrix"))
import validate_data as vd


def test_required_columns_flags_missing():
    rows = [{"uc_id": "UC-1", "category": "F"}]   # missing most cols
    errs = vd.check_required_columns("use-cases.csv", rows, vd.CORE_REQUIRED["use-cases.csv"])
    assert any("short_title" in e for e in errs)
    assert all("use-cases.csv" in e for e in errs)


def test_required_columns_empty():
    assert vd.check_required_columns("x.csv", [], ("a",)) == ["x.csv: empty (no data rows)"]


def test_required_columns_clean():
    rows = [{c: "v" for c in vd.CORE_REQUIRED["identity-catalog.csv"]}]
    assert vd.check_required_columns("identity-catalog.csv", rows, vd.CORE_REQUIRED["identity-catalog.csv"]) == []


def test_unique_flags_duplicate():
    rows = [{"uc_id": "UC-1"}, {"uc_id": "UC-1"}]
    assert vd.check_unique("use-cases.csv", rows, "uc_id") == ["use-cases.csv: duplicate uc_id 'UC-1'"]


def test_enum_flags_invalid_and_allows_blank():
    rows = [{"current_state": "GAP"}, {"current_state": "BOGUS"}, {"current_state": ""}]
    errs = vd.check_enum("current-state.csv", rows, "current_state", vd.VALID_STATES)
    assert errs == ["current-state.csv: invalid current_state 'BOGUS'"]


def test_ids_drops_blanks_and_sentinels():
    assert vd._ids("UC-1;;MISSING-UC;UC-2") == ["UC-1", "UC-2"]


def test_vendor_rows_flags_maturity_and_coverage():
    rows = [{c: "x" for c in vd.VENDOR_REQUIRED}]
    rows[0].update({"target_id": "NHI-1", "maturity": "9", "coverage": ""})
    errs = vd.validate_vendor_rows("v.csv", rows)
    assert any("maturity '9'" in e for e in errs)
    assert any("empty coverage" in e for e in errs)


def test_vendor_rows_accepts_zero_maturity():
    rows = [{c: "x" for c in vd.VENDOR_REQUIRED}]
    rows[0].update({"maturity": "0", "coverage": "GAP"})
    assert vd.validate_vendor_rows("v.csv", rows) == []


def test_vendor_rows_single_slug():
    rows = [dict({c: "x" for c in vd.VENDOR_REQUIRED}, vendor_slug="a", maturity="1", coverage="NATIVE"),
            dict({c: "x" for c in vd.VENDOR_REQUIRED}, vendor_slug="b", maturity="1", coverage="NATIVE")]
    assert any("multiple vendor_slug" in e for e in vd.validate_vendor_rows("v.csv", rows, single_slug=True))


def test_referential_clean():
    uc = [{"uc_id": "UC-F-1", "nhis_in_scope": "NHI-1"}]
    cs = [{"uc_id": "UC-F-1"}]
    idc = [{"nhi_id": "NHI-1"}]
    rt = [{"control_code": "C1", "uc_ids": "UC-F-1;MISSING-UC", "nhi_ids": "NHI-1;MISSING-NHI"}]
    vendors = [("v.csv", [{"target_type": "UC-F", "target_id": "UC-F-1"},
                          {"target_type": "NHI", "target_id": "NHI-1"}])]
    assert vd.validate_referential(uc, cs, rt, idc, vendors) == []


def test_referential_catches_dangling():
    uc = [{"uc_id": "UC-F-1", "nhis_in_scope": "NHI-9"}]   # NHI-9 missing
    cs = [{"uc_id": "UC-F-2"}]                              # not in use-cases
    idc = [{"nhi_id": "NHI-1"}]
    rt = [{"control_code": "C1", "uc_ids": "UC-X", "nhi_ids": "NHI-Y"}]
    vendors = [("v.csv", [{"target_type": "NHI", "target_id": "NHI-Z"}])]
    errs = vd.validate_referential(uc, cs, rt, idc, vendors)
    assert any("NHI-9" in e for e in errs)
    assert any("UC-F-2" in e for e in errs)
    assert any("UC-X" in e for e in errs)
    assert any("NHI-Y" in e for e in errs)
    assert any("NHI-Z" in e for e in errs)


import shutil


def test_validate_all_real_data_is_clean():
    # The shipped data is the golden baseline — zero violations.
    assert vd.validate_all(str(ROOT)) == []


def test_main_exit_zero_on_clean():
    assert vd.main(["--root", str(ROOT)]) == 0


def test_validate_all_accepts_external_data_dir(tmp_path):
    # The gate must validate a non-default domain data dir (e.g. matrix/domains/pam),
    # resolving the shared cross-domain config from <root>/matrix/config. Copying the
    # clean secrets data into an arbitrary dir and validating it there must stay clean.
    ddir = tmp_path / "pam"
    ddir.mkdir()
    for p in (ROOT / "matrix" / "domains" / "secrets").glob("*.csv"):
        shutil.copy(p, ddir / p.name)
    assert vd.validate_all(root=str(ROOT), data_dir=str(ddir)) == []


def test_main_accepts_data_dir_flag(tmp_path):
    ddir = tmp_path / "pam"
    ddir.mkdir()
    for p in (ROOT / "matrix" / "domains" / "secrets").glob("*.csv"):
        shutil.copy(p, ddir / p.name)
    assert vd.main(["--root", str(ROOT), "--data-dir", str(ddir)]) == 0


def test_validate_all_catches_injected_break(tmp_path):
    src = ROOT / "matrix" / "domains" / "secrets"
    dst = tmp_path / "matrix"
    dst.mkdir()
    for p in src.glob("*.csv"):
        shutil.copy(p, dst / p.name)
    # inject a current-state row whose uc_id is not in use-cases
    cs = dst / "current-state.csv"
    cs.write_text(cs.read_text() + "UC-ZZZ-999,GAP,MED,,,,,\n", encoding="utf-8")
    # no descriptor exists under tmp_path -> default resolves to <root>/matrix (the dst)
    viol = vd.validate_all(str(tmp_path))
    assert any("UC-ZZZ-999" in v for v in viol)
    assert vd.main(["--root", str(tmp_path)]) == 1


def test_no_legacy_token_clean():
    cur = [{"uc_id": "UC-1", "current_state": "GAP"}]
    idc = [{"nhi_id": "NHI-1", "sources_likely": "x"}]
    assert vd.check_no_legacy_token(cur, idc) == []


def test_no_legacy_token_flags_old_headers():
    cur = [{"uc_id": "UC-1", "anz_state": "GAP"}]          # legacy column back
    idc = [{"nhi_id": "NHI-1", "sources_at_anz_likely": "x"}]
    errs = vd.check_no_legacy_token(cur, idc)
    assert any("anz_state" in e for e in errs)
    assert any("sources_at_anz_likely" in e for e in errs)


# ---- F3: control-ID verification registry gate ----
_REGISTRY = {
    "asd-ism": {"pattern": r"^ISM-\d{4}$", "controls": ["ISM-0027", "ISM-1139"]},
    "essential-8": {"controls": ["E8-MFA-ML1"]},
}


def test_control_id_registry_flags_unregistered_code():
    trace = [{"framework_slug": "asd-ism", "control_code": "ISM-9999"}]
    errs = vd.check_control_id_registry(trace, _REGISTRY)
    assert any("ISM-9999" in e for e in errs)


def test_control_id_registry_passes_known_code():
    trace = [{"framework_slug": "asd-ism", "control_code": "ISM-0027"}]
    assert vd.check_control_id_registry(trace, _REGISTRY) == []


def test_control_id_registry_flags_unknown_framework():
    trace = [{"framework_slug": "nope", "control_code": "X-1"}]
    assert any("nope" in e for e in vd.check_control_id_registry(trace, _REGISTRY))


def test_control_id_registry_missing_registry_is_violation():
    assert vd.check_control_id_registry([{"framework_slug": "x", "control_code": "y"}], {})


# ---- F2: no uncited provider claims ----
def test_provider_claims_cited_flags_uncited():
    rows = [{"coverage": "NATIVE", "target_id": "UC-1", "vendor_slug": "v",
             "evidence_url": "", "citation_keys": "", "notes": ""}]
    assert any("uncited" in e.lower() for e in vd.check_provider_claims_cited("vc", rows))


def test_provider_claims_cited_accepts_url_citation_or_tag():
    base = {"coverage": "NATIVE", "target_id": "UC-1", "vendor_slug": "v",
            "evidence_url": "", "citation_keys": "", "notes": ""}
    assert vd.check_provider_claims_cited("vc", [{**base, "evidence_url": "http://x"}]) == []
    assert vd.check_provider_claims_cited("vc", [{**base, "citation_keys": "k-2024"}]) == []
    assert vd.check_provider_claims_cited("vc", [{**base, "notes": "[INDUSTRY-CONSENSUS] likely"}]) == []


def test_provider_claims_cited_ignores_non_provider_rows():
    rows = [{"coverage": "GAP", "target_id": "UC-1", "vendor_slug": "v",
             "evidence_url": "", "citation_keys": "", "notes": ""}]
    assert vd.check_provider_claims_cited("vc", rows) == []


# ---- F1/F4: data-provenance manifest ----
_PROV = {"asd-ism": {"as_of": "2026-05-24", "source_tier": "PRIMARY"},
         "vendor-capabilities": {"as_of": "2025", "source_tier": "PRIMARY"}}


def test_data_provenance_flags_missing_entry():
    trace = [{"framework_slug": "essential-8", "control_code": "E8-1"}]
    assert any("essential-8" in e for e in vd.check_data_provenance(trace, _PROV))


def test_data_provenance_flags_invalid_tier():
    trace = [{"framework_slug": "asd-ism", "control_code": "ISM-0027"}]
    prov = {"asd-ism": {"as_of": "2026", "source_tier": "BOGUS"},
            "vendor-capabilities": {"as_of": "2025", "source_tier": "PRIMARY"}}
    assert any("source_tier" in e for e in vd.check_data_provenance(trace, prov))


def test_data_provenance_clean():
    trace = [{"framework_slug": "asd-ism", "control_code": "ISM-0027"}]
    assert vd.check_data_provenance(trace, _PROV) == []


# ---- A1: data-currency gate (max-age per source tier) ----
_POLICY = {"max_age_days": {"PRIMARY": 365, "ANALYST": 270, "CONSENSUS": 180}}


def _prov(as_of, tier="PRIMARY", impact="HIGH", policy=_POLICY):
    p = {"asd-ism": {"as_of": as_of, "source_tier": tier, "impact": impact}}
    if policy is not None:
        p["freshness_policy"] = policy
    return p


def test_data_currency_backdated_high_impact_fails():
    # PRIMARY max age 365d; as_of 2024-01-01 vs today 2026-06-11 is ~892d -> FAIL
    errs = vd.check_data_currency(_prov("2024-01-01"), today="2026-06-11")
    assert len(errs) == 1
    e = errs[0]
    assert "asd-ism" in e and "PRIMARY" in e and "365" in e and "892" in e


def test_data_currency_fresh_fact_passes():
    assert vd.check_data_currency(_prov("2026-05-24"), today="2026-06-11") == []


def test_data_currency_thresholds_come_from_yaml_not_code():
    # Same entry, same age (~200d): passes under PRIMARY=365, fails when the yaml
    # policy tightens PRIMARY to 100 -> the threshold is sourced from the yaml.
    prov_loose = _prov("2025-11-23")  # 200 days before 2026-06-11
    assert vd.check_data_currency(prov_loose, today="2026-06-11") == []
    tight = {"max_age_days": {"PRIMARY": 100, "ANALYST": 270, "CONSENSUS": 180}}
    prov_tight = _prov("2025-11-23", policy=tight)
    errs = vd.check_data_currency(prov_tight, today="2026-06-11")
    assert any("asd-ism" in e and "100" in e for e in errs)


def test_data_currency_tier_thresholds_differ():
    # 200d old: fine for PRIMARY (365), stale for CONSENSUS (180)
    assert vd.check_data_currency(_prov("2025-11-23", tier="PRIMARY"), today="2026-06-11") == []
    errs = vd.check_data_currency(_prov("2025-11-23", tier="CONSENSUS"), today="2026-06-11")
    assert any("CONSENSUS" in e and "180" in e for e in errs)


def test_data_currency_missing_policy_is_violation():
    errs = vd.check_data_currency(_prov("2026-05-24", policy=None), today="2026-06-11")
    assert any("freshness_policy" in e for e in errs)


def test_data_currency_missing_impact_fail_closes_to_high():
    prov = {"freshness_policy": _POLICY,
            "asd-ism": {"as_of": "2024-01-01", "source_tier": "PRIMARY"}}  # no impact key
    assert any("asd-ism" in e for e in vd.check_data_currency(prov, today="2026-06-11"))


def test_data_currency_non_high_impact_not_build_failing():
    assert vd.check_data_currency(_prov("2024-01-01", impact="MEDIUM"), today="2026-06-11") == []


def test_data_currency_year_only_as_of_reads_as_year_end():
    # "2025" resolves to 2025-12-31 (latest date consistent with the declared value):
    # 162d on 2026-06-11 -> fresh under PRIMARY, stale-on-proof under a 100d policy.
    assert vd.check_data_currency(_prov("2025"), today="2026-06-11") == []
    tight = {"max_age_days": {"PRIMARY": 100, "ANALYST": 270, "CONSENSUS": 180}}
    assert vd.check_data_currency(_prov("2025", policy=tight), today="2026-06-11")


def test_data_currency_unparseable_as_of_is_violation():
    errs = vd.check_data_currency(_prov("circa 2025"), today="2026-06-11")
    assert any("as_of" in e for e in errs)


def test_data_currency_today_env_var_injection(monkeypatch):
    # With no explicit today, the gate must honour VALIDATE_DATA_TODAY.
    monkeypatch.setenv("VALIDATE_DATA_TODAY", "2027-06-11")
    assert vd.check_data_currency(_prov("2026-05-24"))  # >365d from injected today
    monkeypatch.setenv("VALIDATE_DATA_TODAY", "2026-06-11")
    assert vd.check_data_currency(_prov("2026-05-24")) == []


def test_data_currency_empty_provenance_defers_to_provenance_gate():
    # check_data_provenance already flags a missing manifest; no double-flag here.
    assert vd.check_data_currency({}, today="2026-06-11") == []


def test_data_currency_invalid_impact_fails_closed_and_flagged():
    # H1: an unrecognised impact value (typo or off-vocabulary) must NOT exempt
    # a stale entry. It fail-closes to HIGH (the entry is gated) AND the bogus
    # value itself is flagged so the typo gets fixed.
    for bogus in ("HIGGH", "CRITICAL"):
        errs = vd.check_data_currency(_prov("2024-01-01", impact=bogus), today="2026-06-11")
        assert any("impact" in e and bogus in e for e in errs), f"impact '{bogus}' not flagged"
        assert any("stale" in e for e in errs), f"impact '{bogus}' silently exempted a stale entry"


def test_data_currency_valid_downgrade_still_exempts():
    # Only an explicit, VALID MEDIUM/LOW exempts an entry from currency gating.
    assert vd.check_data_currency(_prov("2024-01-01", impact="MEDIUM"), today="2026-06-11") == []
    assert vd.check_data_currency(_prov("2024-01-01", impact="LOW"), today="2026-06-11") == []


def test_data_currency_unknown_tier_is_violation_not_skip():
    # M1: a typo'd source_tier must fail closed HERE — check_data_provenance only
    # inspects the current domain's trace, so an off-domain entry with a bad tier
    # would otherwise slip both gates.
    errs = vd.check_data_currency(_prov("2024-01-01", tier="PRIMRY"), today="2026-06-11")
    assert any("source_tier" in e and "PRIMRY" in e for e in errs)


def test_data_currency_empty_env_override_is_clean_error(monkeypatch):
    # L1a: an empty VALIDATE_DATA_TODAY must surface as a clean violation naming
    # the bad value, not an uncaught ValueError traceback.
    monkeypatch.setenv("VALIDATE_DATA_TODAY", "")
    errs = vd.check_data_currency(_prov("2026-05-24"))
    assert any("VALIDATE_DATA_TODAY" in e for e in errs)


def test_data_currency_malformed_env_override_is_clean_error(monkeypatch):
    # L1a: same for a malformed value — the message names the offending value.
    monkeypatch.setenv("VALIDATE_DATA_TODAY", "not-a-date")
    errs = vd.check_data_currency(_prov("2026-05-24"))
    assert any("VALIDATE_DATA_TODAY" in e and "not-a-date" in e for e in errs)


def test_data_currency_env_override_warns_on_stderr(monkeypatch, capsys):
    # L1b: an active (non-empty) override prints a one-line stderr WARNING with
    # the frozen date, so a stray export can't silently freeze the gate.
    monkeypatch.setenv("VALIDATE_DATA_TODAY", "2026-06-11")
    assert vd.check_data_currency(_prov("2026-05-24")) == []
    err = capsys.readouterr().err
    assert "WARNING" in err and "2026-06-11" in err


def test_validate_all_fails_on_backdated_high_impact_fact(monkeypatch):
    # End-to-end: the real manifest validated as of a far-future "today" must
    # trip the currency gate through validate_all (proves it is wired in).
    monkeypatch.setenv("VALIDATE_DATA_TODAY", "2030-01-01")
    viol = vd.validate_all(str(ROOT))
    assert any("max_age_days" in v or "stale" in v for v in viol)


# --- evidence-pack gate (regulatory-driven evidence packs) -----------------

def _trace_row(**kw):
    base = {"framework_slug": "asd-ism", "framework_role": "BACK-MAP",
            "control_code": "ISM-1304", "uc_ids": "UC-P-001", "evidence_item_ids": ""}
    base.update(kw)
    return base


def _cat_row(**kw):
    base = {"ev_id": "EV-PAM-VAULT-REGISTER", "requirement": "a register of vaulted accounts",
            "dimension": "coverage", "tier": "primary", "example_artifact": "",
            "sensitivity_tag": "", "citation_keys": "cyberark-pam-2025"}
    base.update(kw)
    return base


def test_evidence_packs_clean():
    trace = [_trace_row(evidence_item_ids="EV-PAM-VAULT-REGISTER")]
    catalog = [_cat_row()]
    assert vd.check_evidence_packs(trace, catalog) == []


def test_evidence_packs_broken_reference():
    trace = [_trace_row(evidence_item_ids="EV-PAM-VAULT-REGISTER;EV-PAM-GHOST")]
    catalog = [_cat_row()]
    errs = vd.check_evidence_packs(trace, catalog)
    assert any("EV-PAM-GHOST" in e for e in errs)
    assert all("EV-PAM-VAULT-REGISTER" not in e for e in errs)


def test_evidence_packs_uncited_referenced_item_flagged():
    trace = [_trace_row(evidence_item_ids="EV-PAM-VAULT-REGISTER")]
    catalog = [_cat_row(citation_keys="")]
    errs = vd.check_evidence_packs(trace, catalog)
    assert any("EV-PAM-VAULT-REGISTER" in e and "citation" in e.lower() for e in errs)


def test_evidence_packs_invalid_dimension_flagged():
    trace = [_trace_row(evidence_item_ids="EV-PAM-VAULT-REGISTER")]
    catalog = [_cat_row(dimension="bogus")]
    assert any("bogus" in e for e in vd.check_evidence_packs(trace, catalog))


def test_evidence_packs_invalid_tier_flagged():
    trace = [_trace_row(evidence_item_ids="EV-PAM-VAULT-REGISTER")]
    catalog = [_cat_row(tier="headline")]
    assert any("headline" in e for e in vd.check_evidence_packs(trace, catalog))


def test_evidence_packs_skips_adversary_lens_rows():
    # an ADVERSARY-LENS row's evidence refs are not collected (packs are compliance-only)
    trace = [_trace_row(framework_role="ADVERSARY-LENS", evidence_item_ids="EV-PAM-GHOST")]
    catalog = [_cat_row()]
    assert vd.check_evidence_packs(trace, catalog) == []


def test_evidence_packs_optional_when_no_refs():
    # rows without evidence_item_ids must not trip the gate (column is optional)
    trace = [_trace_row(), {"framework_slug": "asd-ism", "framework_role": "BACK-MAP",
                            "control_code": "ISM-1619", "uc_ids": "UC-P-001"}]
    catalog = [_cat_row()]
    assert vd.check_evidence_packs(trace, catalog) == []


# --- H1b: vendor-fit rows must carry a verbatim evidence_quote --------------

_FIT_COLS = ("vendor", "vendor_slug", "area", "fit", "justification",
             "evidence_url", "citation_keys", "evidence_quote")


def _fit_row(**kw):
    base = {"vendor": "Vendor X", "vendor_slug": "vx", "area": "JML", "fit": "NATIVE",
            "justification": "vendor docs say so", "evidence_url": "https://x.example/docs",
            "citation_keys": "vx-docs",
            "evidence_quote": "A verbatim sentence from the vendor's own documentation."}
    base.update(kw)
    return base


def _write_fit(tmp_path, rows, cols=_FIT_COLS):
    with open(tmp_path / "fit.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    return str(tmp_path)


def test_vendor_fit_requires_evidence_quote_column_in_schema():
    # the schema contract itself must demand the quote column
    assert "evidence_quote" in vd.VENDOR_FIT_REQUIRED


def test_vendor_fit_missing_quote_column_is_violation(tmp_path):
    cols = tuple(c for c in _FIT_COLS if c != "evidence_quote")
    d = _write_fit(tmp_path, [_fit_row()], cols=cols)
    errs = vd.check_vendor_fit(d, "fit.csv")
    assert any("evidence_quote" in e and "missing required column" in e for e in errs)


def test_vendor_fit_empty_quote_is_violation(tmp_path):
    d = _write_fit(tmp_path, [_fit_row(evidence_quote="")])
    errs = vd.check_vendor_fit(d, "fit.csv")
    assert any("evidence_quote" in e and "vx/JML" in e for e in errs)


def test_vendor_fit_complete_row_with_quote_is_clean(tmp_path):
    d = _write_fit(tmp_path, [_fit_row()])
    assert vd.check_vendor_fit(d, "fit.csv") == []


# --- H1c: quote_type honesty flag on regulatory-trace rows -------------------

def test_quote_type_enum_is_the_closed_set():
    assert vd.VALID_QUOTE_TYPES == {"verbatim", "paraphrase", "analyst-note"}


def test_quote_type_column_is_required_schema():
    assert "quote_type" in vd.CORE_REQUIRED["regulatory-trace.csv"]


def test_quote_type_invalid_value_is_violation():
    rows = [{"control_code": "C1", "quote_type": "vibes"}]
    errs = vd.check_quote_type("regulatory-trace.csv", rows)
    assert any("vibes" in e and "C1" in e for e in errs)


def test_quote_type_empty_value_is_violation():
    rows = [{"control_code": "C1", "quote_type": ""}]
    assert vd.check_quote_type("regulatory-trace.csv", rows)


def test_quote_type_accepts_every_member_of_the_closed_set():
    # an analyst-note row is ACCEPTED (honest label), exactly like verbatim —
    # H1d's quote-presence rules only ever bind rows labelled verbatim
    rows = [{"control_code": f"C{i}", "quote_type": qt}
            for i, qt in enumerate(sorted(vd.VALID_QUOTE_TYPES))]
    assert vd.check_quote_type("regulatory-trace.csv", rows) == []


def test_quote_type_missing_column_defers_to_required_columns_check():
    # no double-flag: column absence is check_required_columns' job
    rows = [{"control_code": "C1"}]
    assert vd.check_quote_type("regulatory-trace.csv", rows) == []
    errs = vd.check_required_columns("regulatory-trace.csv", rows,
                                     vd.CORE_REQUIRED["regulatory-trace.csv"])
    assert any("quote_type" in e for e in errs)


def test_validate_all_catches_bad_quote_type(tmp_path):
    import shutil
    dst = tmp_path / "matrix"
    dst.mkdir()
    for p in (ROOT / "matrix" / "domains" / "secrets").glob("*.csv"):
        shutil.copy(p, dst / p.name)
    rt = dst / "regulatory-trace.csv"
    text = rt.read_text(encoding="utf-8")
    assert ",verbatim" in text
    rt.write_text(text.replace(",verbatim", ",vibes", 1), encoding="utf-8")
    viol = vd.validate_all(str(tmp_path))
    assert any("quote_type" in v and "vibes" in v for v in viol)
