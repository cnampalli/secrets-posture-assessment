#!/usr/bin/env python3
"""Read-only CSV schema + referential-integrity validator for the matrix data contracts.

Pure check functions return lists of violation strings (empty = clean); validate_all
aggregates; the CLI exits 1 on any violation. Mirrors methodology/validate_rubric.py.
Read-only — never mutates data.

CLI: python3 matrix/validate_data.py [--root .]
"""
import argparse
import csv
import datetime
import glob
import os
import re
import sys

import yaml

import identity_spine

# M2 identity-spine archetype classes (matches config/identity-spine.yaml).
VALID_IDENTITY_CLASSES = ("human", "npe", "agentic")

# Closed npe_conformance vocabulary — matches the legend rendered in the stakeholder
# pack (build_stakeholder_pack.py npe_conformance legend). Off-legend values (e.g. a
# bare "NPE") must fail the gate so a cross-domain conformance claim stays truthful.
VALID_NPE_CONFORMANCE = {"CONFORMANT", "HUMAN-IDENTITY", "CREDENTIAL-NOT-IDENTITY",
                         "CROSS-CUTTING-ATTRIBUTE", "HUMAN-USE-ANTIPATTERN"}

CORE_REQUIRED = {
    "use-cases.csv": ("uc_id", "category", "short_title", "story", "acceptance_criteria",
                      "nhis_in_scope", "outcome_lens", "backmap_codes", "priority_fi", "citation_keys"),
    "current-state.csv": ("uc_id", "current_state", "confidence", "evidence_q_ids",
                              "evidence_redacted", "gap_notes", "sensitivity_tag", "citation_keys"),
    "regulatory-trace.csv": ("framework_slug", "framework_role", "control_code", "control_short_title",
                             "uc_ids", "nhi_ids", "maturity_level", "evidence_url", "evidence_quote",
                             "citation_keys", "quote_type"),
    "identity-catalog.csv": ("nhi_id", "bucket", "short_name", "description", "typical_secrets",
                             "lifecycle", "governance_maturity", "sources_likely", "citation_keys",
                             "spine_id"),
}
VENDOR_REQUIRED = ("vendor_slug", "vendor_name", "target_id", "target_type", "coverage",
                   "maturity", "evidence_url", "evidence_quote", "citation_keys", "notes")
VALID_STATES = {"MET", "PARTIAL", "GAP", "PENDING", "NA"}
# INFORMATIVE (context-only ISO mappings) and THREAT-CONTEXT (adversary/incident
# framing) are deliberate, documented IGA roles. Like ADVERSARY-LENS, they do NOT
# bind evidence packs — EVIDENCE_COMPLIANCE_ROLES below stays compliance-only.
VALID_ROLES = {"PRIMARY-LENS", "BACK-MAP", "ADVERSARY-LENS", "INFORMATIVE", "THREAT-CONTEXT"}
SENTINELS = {"MISSING-UC", "MISSING-NHI"}

# --- evidence-pack gate (regulatory-driven evidence packs) ---
# Evidence packs are a compliance-evidence concept, so refs are collected only
# from compliance-role rows; ADVERSARY-LENS rows are skipped.
EVIDENCE_COMPLIANCE_ROLES = {"PRIMARY-LENS", "BACK-MAP"}
# "scope" is a deliberate IGA evidence dimension (breadth of population/system in scope).
VALID_EVIDENCE_DIMENSIONS = {"coverage", "enforcement", "depth", "cadence", "governance",
                             "exception", "scope"}
VALID_EVIDENCE_TIERS = {"primary", "follow-up"}

# --- provenance gate (theme F) ---
PROVIDER_COVERAGE = {"NATIVE", "ADD-ON", "PARTNER"}      # claims that need a source
VALID_SOURCE_TIERS = {"PRIMARY", "ANALYST", "CONSENSUS"}
# H1c: every regulatory-trace evidence_quote declares its honesty class. Only
# `verbatim` rows are (later, H1d) held to source-quote presence/fidelity;
# `paraphrase` and `analyst-note` are honest non-verbatim labels, never
# silently passed off as source wording.
VALID_QUOTE_TYPES = {"verbatim", "paraphrase", "analyst-note"}
VALID_IMPACT_LEVELS = {"HIGH", "MEDIUM", "LOW"}          # currency-gate impact vocabulary (closed)
INFERENCE_TAGS = ("[INDUSTRY-CONSENSUS]", "[CONSENSUS]", "[INFERRED]", "[INFER")
PROVENANCE_EXTRA_KEYS = ("vendor-capabilities",)         # non-framework data sources

# --- H1a: citation-key resolution gate ----------------------------------
# Every citation_keys token in the data must resolve to a @key defined in
# meta/citations.bib, EXCEPT the sentinel status-markers below. Sentinels are
# deliberate honesty flags, not citations — they mark a control row whose
# source verification is intentionally outstanding, and they must NEVER gain a
# bib entry (that would fake a source). Anything else dangling fails the build.
CITATION_SENTINEL_ALLOWLIST = {
    # ISO 27001 Annex A control mappings recorded before the controls' wording
    # could be verified against licensed standard text (WS1 deferred item):
    "iso-27001-a5-3-unverified",    # A.5.3 segregation of duties — mapping unverified
    "iso-27001-a5-15-unverified",   # A.5.15 access control — mapping unverified
    "iso-27001-a5-16-unverified",   # A.5.16 identity management — mapping unverified
    # A.5.18 access rights — mapped, but the (licensed) quote is withheld:
    "iso-27001-a5-18-quote-withheld",
}
_BIB_KEY_RE = re.compile(r"@\w+\{([^,\s]+),")


def load_csv(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def load_yaml(path):
    """Load a YAML mapping; return {} if the file is absent."""
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def _ids(value):
    """Split a ;-list, dropping blanks and intentional sentinels."""
    return [t.strip() for t in (value or "").split(";")
            if t.strip() and t.strip() not in SENTINELS]


def check_required_columns(name, rows, required):
    if not rows:
        return [f"{name}: empty (no data rows)"]
    have = set(rows[0].keys())
    return [f"{name}: missing required column '{c}'" for c in required if c not in have]


def check_unique(name, rows, key):
    seen, errs = set(), []
    for r in rows:
        v = r.get(key, "")
        if v in seen:
            errs.append(f"{name}: duplicate {key} '{v}'")
        seen.add(v)
    return errs


def check_enum(name, rows, col, allowed):
    errs = []
    for r in rows:
        v = (r.get(col) or "").strip()
        if v and v not in allowed:
            errs.append(f"{name}: invalid {col} '{v}'")
    return errs


def validate_vendor_rows(name, rows, single_slug=False):
    """Per-vendor / aggregate row checks: required cols, maturity 0-5, non-empty coverage,
    and (per-vendor only) a single consistent vendor_slug."""
    errs = check_required_columns(name, rows, VENDOR_REQUIRED)
    if errs:
        return errs   # missing columns -> key access below is unsafe
    slugs = set()
    for r in rows:
        tid = r.get("target_id", "?")
        m = (r.get("maturity") or "").strip()
        if not (m.isdigit() and 0 <= int(m) <= 5):
            errs.append(f"{name}: maturity '{m}' not integer 0-5 (target {tid})")
        if not (r.get("coverage") or "").strip():
            errs.append(f"{name}: empty coverage (target {tid})")
        slugs.add((r.get("vendor_slug") or "").strip())
    if single_slug and len(slugs) > 1:
        errs.append(f"{name}: multiple vendor_slug values {sorted(slugs)} in one per-vendor file")
    return errs


def resolve_domain_descriptor(root, data_dir):
    """Find the domain descriptor (config/domains/*.yaml) whose `data_dir` resolves
    to the data dir under validation; return the raw YAML mapping, or None.

    Descriptor `data_dir` values are relative to <root>/matrix (secrets' is ".",
    meaning <root>/matrix itself); both sides are realpath'd before comparing.
    This is THE definition of which domain a --data-dir belongs to — properties
    like the matrix-less exception are declared in the descriptor, never inferred
    from filenames lying around in the data dir."""
    target = os.path.realpath(data_dir)
    cfg_dir = os.path.join(root, "matrix", "config", "domains")
    if not os.path.isdir(cfg_dir):
        return None
    for fn in sorted(os.listdir(cfg_dir)):
        if not fn.endswith((".yaml", ".yml")):
            continue
        d = load_yaml(os.path.join(cfg_dir, fn))
        dd = os.path.realpath(os.path.join(root, "matrix", d.get("data_dir") or ""))
        if dd == target:
            return d
    return None


def default_data_dir(root):
    """Resolve the no-arg default data dir VIA THE secrets descriptor, so a bare
    `python3 matrix/validate_data.py` keeps meaning "validate the secrets domain"
    after its CSVs moved to matrix/domains/secrets/. The descriptor's `data_dir`
    is relative to <root>/matrix; fall back to <root>/matrix if it's unreadable."""
    d = load_yaml(os.path.join(root, "matrix", "config", "domains", "secrets.yaml"))
    return os.path.join(root, "matrix", d.get("data_dir") or ".")


def check_aggregate_vendor_capabilities(rows, vendor_fit=None):
    """NARROW exception to the 'empty (no data rows)' rule, for the aggregate
    vendor-capabilities.csv only: a header-only file is accepted IFF the domain's
    descriptor declares a `vendor_fit` grid (the bespoke per-area substitute for
    the matrix, e.g. IGA's iga-vendor-fit.csv — itself gated by check_vendor_fit).
    Everything else is unchanged — an empty vendor matrix in a domain without a
    declared fit grid stays a violation, and any data rows present (even in a
    matrix-less domain) are fully validated. Downstream per-row vendor checks
    naturally no-op on the empty row list."""
    if not rows and vendor_fit:
        return []
    return validate_vendor_rows("vendor-capabilities.csv", rows)


_AGG_COMPARE = ("coverage", "maturity", "evidence_url", "evidence_quote", "citation_keys")


def check_aggregate_vendor_consistency(agg_rows, per_vendor):
    """H6 gate: the aggregate vendor-capabilities.csv must equal the UNION of the
    per-vendor vendor-capabilities-<slug>.csv files — same rows (keyed by
    vendor_slug+target_id) with the same coverage/maturity/evidence. Catches the
    drift class where a per-vendor edit is not propagated to the aggregate (the
    Britive sync gap). A header-only aggregate (matrix-less domain) is exempt."""
    if not agg_rows:
        return []
    key = lambda r: ((r.get("vendor_slug") or "").strip(), (r.get("target_id") or "").strip())
    sig = lambda r: tuple((c, (r.get(c) or "").strip()) for c in _AGG_COMPARE)
    agg = {key(r): sig(r) for r in agg_rows}
    pv = {}
    for _name, rows in per_vendor:
        for r in rows:
            pv[key(r)] = sig(r)
    errs = []
    for k in sorted(set(agg) - set(pv)):
        errs.append(f"vendor-capabilities.csv: row {k[0]}/{k[1]} is in the aggregate but no "
                    f"per-vendor file — stale aggregate row")
    for k in sorted(set(pv) - set(agg)):
        errs.append(f"vendor-capabilities.csv: row {k[0]}/{k[1]} is in a per-vendor file but "
                    f"missing from the aggregate — un-synced (regenerate the aggregate)")
    for k in sorted(set(agg) & set(pv)):
        if agg[k] != pv[k]:
            errs.append(f"vendor-capabilities.csv: row {k[0]}/{k[1]} differs between the aggregate "
                        f"and its per-vendor file (coverage/maturity/evidence drift)")
    return errs


# --- descriptor-declared vendor-fit grid (matrix-less domains) ---
# The fit grid is the load-bearing substitute for the vendor matrix, so its
# claims clear the same anti-fabrication bar: valid grade + sourced, every row.
VENDOR_FIT_REQUIRED = ("vendor", "vendor_slug", "area", "fit", "justification",
                       "evidence_url", "citation_keys", "evidence_quote")
VALID_FIT_GRADES = {"NATIVE", "PARTIAL", "ADD-ON"}


def check_vendor_fit(data_dir, fit_name):
    """Validate a descriptor-declared vendor-fit grid. Declared means load-bearing:
    the file must exist with data rows (a missing/header-only fit grid alongside a
    header-only matrix would leave the domain with NO vendor evidence), carry the
    required columns, use a valid fit grade, and source every claim (justification
    + evidence_url + citation_keys + a verbatim evidence_quote, H1b)."""
    path = os.path.join(data_dir, fit_name)
    if not os.path.exists(path):
        return [f"{fit_name}: declared in the domain descriptor but missing"]
    rows = load_csv(path)
    errs = check_required_columns(fit_name, rows, VENDOR_FIT_REQUIRED)
    if errs:
        return errs   # empty file / missing columns -> per-row checks are unsafe
    for r in rows:
        where = f"{r.get('vendor_slug') or '?'}/{r.get('area') or '?'}"
        fit = (r.get("fit") or "").strip()
        if fit not in VALID_FIT_GRADES:
            errs.append(f"{fit_name}: invalid fit '{fit}' ({where}) — expected one of "
                        f"{sorted(VALID_FIT_GRADES)}")
        for col in ("justification", "evidence_url", "citation_keys", "evidence_quote"):
            if not (r.get(col) or "").strip():
                errs.append(f"{fit_name}: empty {col} ({where}) — a fit claim without "
                            f"a source is a violation")
    return errs


def check_quote_type(name, rows):
    """H1c gate: every regulatory-trace row must label its evidence_quote with a
    quote_type from the closed set VALID_QUOTE_TYPES (non-empty). A missing
    column is check_required_columns' job (no double-flag here); when the
    column exists, every row must carry a valid value."""
    if not rows or "quote_type" not in rows[0]:
        return []
    errs = []
    for r in rows:
        v = (r.get("quote_type") or "").strip()
        if v not in VALID_QUOTE_TYPES:
            errs.append(f"{name}: invalid quote_type '{v}' (control "
                        f"{r.get('control_code', '?')}) — expected one of "
                        f"{sorted(VALID_QUOTE_TYPES)}")
    return errs


def validate_referential(use_cases, current_state, reg_trace, identity, vendor_files):
    """Cross-file integrity: uc_id / nhi_id references resolve (sentinels skipped)."""
    errs = []
    uc_ids = {r.get("uc_id", "") for r in use_cases}
    nhi_ids = {r.get("nhi_id", "") for r in identity}
    cs_ids = {r.get("uc_id", "") for r in current_state}
    for i in sorted(cs_ids - uc_ids):
        errs.append(f"current-state.csv: uc_id '{i}' not in use-cases")
    for i in sorted(uc_ids - cs_ids):
        errs.append(f"current-state.csv: missing uc_id '{i}' present in use-cases")
    for r in reg_trace:
        cc = r.get("control_code", "?")
        for u in _ids(r.get("uc_ids")):
            if u not in uc_ids:
                errs.append(f"regulatory-trace.csv: uc_id '{u}' (control {cc}) not in use-cases")
        for n in _ids(r.get("nhi_ids")):
            if n not in nhi_ids:
                errs.append(f"regulatory-trace.csv: nhi_id '{n}' (control {cc}) not in identity-catalog")
    for r in use_cases:
        for n in _ids(r.get("nhis_in_scope")):
            if n not in nhi_ids:
                errs.append(f"use-cases.csv: nhis_in_scope '{n}' (uc {r.get('uc_id')}) not in identity-catalog")
    for name, rows in vendor_files:
        for r in rows:
            tt = (r.get("target_type") or "").strip()
            tid = (r.get("target_id") or "").strip()
            if tt == "NHI" and tid not in nhi_ids:
                errs.append(f"{name}: target_id '{tid}' (NHI) not in identity-catalog")
            elif tt.startswith("UC") and tid not in uc_ids:
                errs.append(f"{name}: target_id '{tid}' (UC) not in use-cases")
    return errs


def check_no_legacy_token(current_state, identity):
    """Fail if a legacy ANZ-era header has crept back into the data (WS-5b rename guard)."""
    errs = []
    cur_cols = set(current_state[0].keys()) if current_state else set()
    idc_cols = set(identity[0].keys()) if identity else set()
    if "anz_state" in cur_cols:
        errs.append("current-state.csv: legacy column 'anz_state' present (use 'current_state')")
    if "sources_at_anz_likely" in idc_cols:
        errs.append("identity-catalog.csv: legacy column 'sources_at_anz_likely' present (use 'sources_likely')")
    return errs


def check_control_id_registry(trace, registry):
    """F3 anti-fabrication gate: every (framework, control_code) in the trace must be
    in the verified registry, or the build fails. Optional per-framework `pattern`
    adds a structural check. A missing/empty registry is itself a violation."""
    if not registry:
        return ["control-id-registry.yaml: missing or empty — F3 control-ID gate cannot run"]
    errs = []
    for r in trace:
        fw = (r.get("framework_slug") or "").strip()
        cc = (r.get("control_code") or "").strip()
        entry = registry.get(fw)
        if not entry:
            errs.append(f"regulatory-trace.csv: framework '{fw}' has no control-id-registry entry "
                        f"(control {cc})")
            continue
        allowed = set(entry.get("controls") or [])
        if cc not in allowed:
            errs.append(f"regulatory-trace.csv: control_code '{cc}' (framework {fw}) is NOT in the "
                        f"verified registry — possible fabrication/typo; verify and register it")
        pat = entry.get("pattern")
        if pat and cc and not re.match(pat, cc):
            errs.append(f"regulatory-trace.csv: control_code '{cc}' (framework {fw}) does not match "
                        f"verified pattern {pat}")
    return errs


def _normalize_semantic(s):
    """lower-case + collapse whitespace, for substring topic matching."""
    return re.sub(r"\s+", " ", (s or "").strip().lower())


def check_control_semantics(trace, semantics):
    """F3 semantic gate (H2): a control's recorded text must match what the control
    is ABOUT. For every trace row whose (framework_slug, control_code) has an
    `expect_substring` in control-semantics.yaml, that substring — normalised
    (lower-case, whitespace-collapsed) — MUST appear in the row's control_short_title
    + evidence_quote. This makes the right-ID-wrong-text class (the audit's HIGH-2:
    CPS234-§22 carrying §21's text) a build failure. Controls with no registered
    expectation are not gated, so the registry can be seeded incrementally. A
    missing/empty registry is itself a violation (fail-closed)."""
    if not semantics:
        return ["control-semantics.yaml: missing or empty — H2 semantic-control gate cannot run"]
    errs = []
    for r in trace:
        fw = (r.get("framework_slug") or "").strip()
        cc = (r.get("control_code") or "").strip()
        exp = (semantics.get(fw) or {}).get(cc)
        if not exp:
            continue
        haystack = _normalize_semantic((r.get("control_short_title") or "") + " "
                                       + (r.get("evidence_quote") or ""))
        if _normalize_semantic(exp) not in haystack:
            errs.append(f"regulatory-trace.csv: control {cc} ({fw}) text does not match its "
                        f"registered topic — expected substring \"{exp}\" in "
                        f"control_short_title+evidence_quote; possible right-ID-wrong-text "
                        f"(verify the row, or update control-semantics.yaml)")
    return errs


def check_provider_claims_cited(name, rows):
    """F2 gate: a capability claim (NATIVE/ADD-ON/PARTNER) must carry a source —
    an evidence_url, a citation_key, or an explicit inference tag in notes."""
    errs = []
    for r in rows:
        if (r.get("coverage") or "").strip() not in PROVIDER_COVERAGE:
            continue
        url = (r.get("evidence_url") or "").strip()
        cit = (r.get("citation_keys") or "").strip()
        notes = r.get("notes") or ""
        if url or cit or any(t in notes for t in INFERENCE_TAGS):
            continue
        errs.append(f"{name}: uncited {r.get('coverage')} claim (target {r.get('target_id', '?')}, "
                    f"vendor {r.get('vendor_slug', '?')}) — no evidence_url, citation_keys, or inference tag")
    return errs


def check_ownership_sources(ownership):
    """H4 gate: every ACQUISITION edge in vendor-ownership.yaml (one carrying an
    `as_of` date) MUST cite a primary-source `source_url` (http/https). First-party
    'own product' edges (no as_of) are exempt. Ownership config is optional, so an
    empty map is not itself a violation — but a dated edge without a source is, the
    rule that keeps an unsourced M&A claim (the Entro error) out of the report."""
    if not ownership:
        return []
    errs = []
    for slug, edge in ownership.items():
        if not isinstance(edge, dict) or not edge.get("as_of"):
            continue
        url = str(edge.get("source_url") or "").strip()
        if not re.match(r"^https?://", url):
            errs.append(f"vendor-ownership.yaml: edge '{slug}' -> '{edge.get('parent', '?')}' "
                        f"is a dated acquisition (as_of {edge.get('as_of')}) with no primary-source "
                        f"source_url — every acquisition edge must cite one")
    return errs


def check_data_provenance(trace, provenance):
    """F1/F4 gate: every framework in the trace and each non-framework data source must
    have a provenance entry with a non-empty as_of and a valid source_tier."""
    if not provenance:
        return ["data-provenance.yaml: missing or empty — F1/F2 provenance gate cannot run"]
    needed = {(r.get("framework_slug") or "").strip() for r in trace} | set(PROVENANCE_EXTRA_KEYS)
    errs = []
    for key in sorted(k for k in needed if k):
        e = provenance.get(key)
        if not e:
            errs.append(f"data-provenance.yaml: missing provenance entry for '{key}'")
            continue
        if not str(e.get("as_of", "")).strip():
            errs.append(f"data-provenance.yaml: '{key}' missing as_of date")
        tier = (e.get("source_tier") or "").strip()
        if tier not in VALID_SOURCE_TIERS:
            errs.append(f"data-provenance.yaml: '{key}' invalid/missing source_tier '{tier}' "
                        f"(expected one of {sorted(VALID_SOURCE_TIERS)})")
    return errs


# --- data-currency gate (A1): max-age per source tier --------------------
# A dated claim goes stale; a stale HIGH-impact claim is a release blocker.
# Thresholds live in data-provenance.yaml under `freshness_policy.max_age_days`
# (per source_tier) — NEVER hard-coded here. Entries may declare `impact:`
# (closed vocabulary VALID_IMPACT_LEVELS); a missing OR unrecognised impact
# fail-closes to HIGH, so only an explicit, valid MEDIUM/LOW downgrade exempts
# an entry from the build gate.

def _reference_today(today=None):
    """Resolve the gate's reference date. Precedence: explicit arg >
    VALIDATE_DATA_TODAY env var (ISO date, for deterministic tests/CI replays) >
    the real current date. An active env override prints a one-line stderr
    WARNING (a stray export must not silently freeze the clock); an empty or
    malformed override raises ValueError with a clean message naming the bad
    value — callers convert that to a violation rather than a traceback."""
    if today:
        if isinstance(today, datetime.date):
            return today
        return datetime.date.fromisoformat(str(today).strip())
    value = os.environ.get("VALIDATE_DATA_TODAY")
    if value is None:
        return datetime.date.today()
    try:
        ref = datetime.date.fromisoformat(value.strip())
    except ValueError:
        raise ValueError(f"VALIDATE_DATA_TODAY override '{value}' is not a valid "
                         f"ISO date (YYYY-MM-DD)") from None
    print(f"WARNING: VALIDATE_DATA_TODAY override active — currency clock frozen "
          f"at {ref.isoformat()}", file=sys.stderr)
    return ref


def _parse_as_of(value):
    """Parse an as_of value to a date, or None if unparseable.
    A bare year (e.g. "2025") resolves to that year's LAST day — the latest
    date consistent with the declared value, so the gate only fails on
    provable staleness rather than fabricating precision the data lacks."""
    s = str(value or "").strip()
    if re.fullmatch(r"\d{4}", s):
        return datetime.date(int(s), 12, 31)
    try:
        return datetime.date.fromisoformat(s)
    except ValueError:
        return None


def check_data_currency(provenance, today=None):
    """A1 build gate: fail when a HIGH-impact provenance entry's as_of is older
    than its source_tier's max_age_days from freshness_policy. An absent/empty
    manifest is already flagged by check_data_provenance (no double-flag)."""
    if not provenance:
        return []
    policy = (provenance.get("freshness_policy") or {}).get("max_age_days") or {}
    if not policy:
        return ["data-provenance.yaml: missing freshness_policy.max_age_days — "
                "data-currency gate cannot run"]
    try:
        ref = _reference_today(today)
    except ValueError as exc:
        return [f"{exc} — data-currency gate cannot run"]
    errs = []
    for key in sorted(k for k in provenance if k != "freshness_policy"):
        e = provenance.get(key) or {}
        impact = (str(e.get("impact") or "HIGH")).strip().upper()  # fail-closed default
        if impact not in VALID_IMPACT_LEVELS:
            # unrecognised impact fails CLOSED: flag the bad value AND gate the
            # entry as HIGH — only an explicit, valid downgrade exempts it
            errs.append(f"data-provenance.yaml: '{key}' invalid impact '{e.get('impact')}' "
                        f"(expected one of {sorted(VALID_IMPACT_LEVELS)}) — treated as HIGH")
            impact = "HIGH"
        if impact != "HIGH":
            continue
        as_of = _parse_as_of(e.get("as_of"))
        if as_of is None:
            errs.append(f"data-provenance.yaml: '{key}' as_of '{e.get('as_of')}' is not a "
                        f"parseable date (YYYY-MM-DD or YYYY) — currency gate cannot date it")
            continue
        tier = (e.get("source_tier") or "").strip()
        if tier not in VALID_SOURCE_TIERS:
            # an unrecognised tier must fail closed HERE, not be deferred:
            # check_data_provenance only inspects the current domain's trace, so
            # an off-domain entry with a typo'd tier would slip both gates
            errs.append(f"data-provenance.yaml: '{key}' invalid/missing source_tier '{tier}' "
                        f"(expected one of {sorted(VALID_SOURCE_TIERS)}) — currency gate "
                        f"cannot age it")
            continue
        max_age = policy.get(tier)
        if max_age is None:
            # a VALID tier missing from the policy is a policy hole -> fail closed
            errs.append(f"data-provenance.yaml: freshness_policy.max_age_days has no "
                        f"threshold for tier '{tier}' (entry '{key}')")
            continue
        age = (ref - as_of).days
        if age > int(max_age):
            errs.append(f"data-provenance.yaml: '{key}' is stale — as_of {as_of.isoformat()} "
                        f"is {age} days old, exceeding {tier} max_age_days {max_age} "
                        f"(re-verify the source and refresh as_of)")
    return errs


def check_citation_keys_resolve(bib_path, files):
    """H1a gate: every citation_keys token used in the given (name, rows) files
    must resolve to a @key defined in the bibliography at `bib_path` or be an
    allowlisted sentinel (CITATION_SENTINEL_ALLOWLIST). A missing bibliography
    fails closed — the gate cannot certify resolution without it. Each dangling
    (file, key) pair is reported once."""
    if not os.path.exists(bib_path):
        return [f"{bib_path}: citations bibliography missing — "
                f"citation-key resolution gate cannot run"]
    with open(bib_path, encoding="utf-8") as fh:
        defined = set(_BIB_KEY_RE.findall(fh.read()))
    errs, seen = [], set()
    for name, rows in files:
        for r in rows:
            for key in (t.strip() for t in (r.get("citation_keys") or "").split(";")):
                if not key or key in defined or key in CITATION_SENTINEL_ALLOWLIST:
                    continue
                if (name, key) in seen:
                    continue
                seen.add((name, key))
                errs.append(f"{name}: citation key '{key}' is not defined in "
                            f"meta/citations.bib and is not an allowlisted sentinel")
    return errs


def check_evidence_packs(trace, catalog):
    """Regulatory-driven evidence-pack gate. Validates that every `evidence_item_ids`
    referenced by a compliance-role control row resolves to an `ev_id` in the evidence
    catalog and that each referenced item carries a citation; also enum-checks every
    catalog item's `dimension`/`tier`. The `evidence_item_ids` column is optional —
    rows without it are skipped, so domains with no packs stay clean."""
    errs = []
    by_id = {(r.get("ev_id") or "").strip(): r for r in catalog}

    # enum checks across the whole catalog (a malformed item is wrong regardless of use)
    for r in catalog:
        ev = (r.get("ev_id") or "").strip()
        dim = (r.get("dimension") or "").strip()
        tier = (r.get("tier") or "").strip()
        if dim and dim not in VALID_EVIDENCE_DIMENSIONS:
            errs.append(f"evidence-catalog.csv: invalid dimension '{dim}' (item {ev})")
        if tier and tier not in VALID_EVIDENCE_TIERS:
            errs.append(f"evidence-catalog.csv: invalid tier '{tier}' (item {ev})")

    # reference resolution + citation, collected only from compliance-role rows
    for row in trace:
        if (row.get("framework_role") or "").strip() not in EVIDENCE_COMPLIANCE_ROLES:
            continue
        cc = row.get("control_code", "?")
        for ev in _ids(row.get("evidence_item_ids")):
            item = by_id.get(ev)
            if item is None:
                errs.append(f"regulatory-trace.csv: evidence_item_ids '{ev}' (control {cc}) "
                            f"not in evidence-catalog.csv")
                continue
            if not (item.get("citation_keys") or "").strip():
                errs.append(f"evidence-catalog.csv: item '{ev}' (referenced by control {cc}) "
                            f"has no citation_keys")
    return errs


def check_identity_spine_registry(spine):
    """M2: the identity-spine archetype registry is well-formed. Returns violation strings
    (empty = clean). Fail-closed: an empty/missing registry is itself a violation so the
    cross-domain identity gate can never silently no-op."""
    archetypes = spine.get("archetypes") or []
    if not archetypes:
        return ["identity-spine.yaml: missing or empty — identity-spine gate cannot run"]
    errs = []
    seen = set()
    for a in archetypes:
        sid = (a.get("spine_id") or "").strip()
        if not sid:
            errs.append("identity-spine.yaml: archetype with empty spine_id")
            continue
        if sid in seen:
            errs.append(f"identity-spine.yaml: duplicate spine_id {sid}")
        seen.add(sid)
        if a.get("identity_class") not in VALID_IDENTITY_CLASSES:
            errs.append(f"identity-spine.yaml: {sid} identity_class "
                        f"{a.get('identity_class')!r} not in {VALID_IDENTITY_CLASSES}")
        if not isinstance(a.get("privileged"), bool):
            errs.append(f"identity-spine.yaml: {sid} privileged must be a bool, got "
                        f"{a.get('privileged')!r}")
        for col in ("label", "description", "csa_nhi_anchor"):
            if not (a.get(col) or "").strip():
                errs.append(f"identity-spine.yaml: {sid} missing {col}")
    return errs


def check_identity_spine_mapping(identity_rows, spine):
    """M2: every identity-catalog row maps to a registered archetype or the explicit
    NOT-AN-IDENTITY sentinel (credentials/attributes that aren't identities). Returns
    violation strings (empty = clean)."""
    by_id = spine.get("by_id") or {}
    errs = []
    for r in identity_rows:
        nhi = (r.get("nhi_id") or "").strip()
        sid = (r.get("spine_id") or "").strip()
        if not sid:
            errs.append(f"identity-catalog.csv: {nhi} has empty spine_id")
        elif sid != identity_spine.NOT_AN_IDENTITY and sid not in by_id:
            errs.append(f"identity-catalog.csv: {nhi} spine_id {sid} is not a registered "
                        "archetype (nor the NOT-AN-IDENTITY sentinel)")
    return errs


def validate_all(root=".", data_dir=None):
    """Run all checks against a domain's five CSVs; return all violations.

    `data_dir` is where the domain's CSVs live (default: the secrets domain's
    data_dir, resolved via its descriptor — matrix/domains/secrets). The
    provenance config (control-ID registry + data-provenance manifest) is
    cross-domain and always resolved from `<root>/matrix/config`.
    """
    m = data_dir or default_data_dir(root)
    use_cases = load_csv(os.path.join(m, "use-cases.csv"))
    current = load_csv(os.path.join(m, "current-state.csv"))
    trace = load_csv(os.path.join(m, "regulatory-trace.csv"))
    identity = load_csv(os.path.join(m, "identity-catalog.csv"))

    errs = []
    errs += check_required_columns("use-cases.csv", use_cases, CORE_REQUIRED["use-cases.csv"])
    errs += check_unique("use-cases.csv", use_cases, "uc_id")
    errs += check_required_columns("current-state.csv", current, CORE_REQUIRED["current-state.csv"])
    errs += check_unique("current-state.csv", current, "uc_id")
    errs += check_enum("current-state.csv", current, "current_state", VALID_STATES)
    errs += check_required_columns("regulatory-trace.csv", trace, CORE_REQUIRED["regulatory-trace.csv"])
    errs += check_enum("regulatory-trace.csv", trace, "framework_role", VALID_ROLES)
    errs += check_quote_type("regulatory-trace.csv", trace)
    errs += check_required_columns("identity-catalog.csv", identity, CORE_REQUIRED["identity-catalog.csv"])
    errs += check_unique("identity-catalog.csv", identity, "nhi_id")
    errs += check_enum("identity-catalog.csv", identity, "npe_conformance", VALID_NPE_CONFORMANCE)

    # matrix-less exception is descriptor-declared (vendor_fit key), never inferred
    descriptor = resolve_domain_descriptor(root, m) or {}
    vendor_fit = descriptor.get("vendor_fit") or None

    vendor_files = []
    agg_rows = load_csv(os.path.join(m, "vendor-capabilities.csv"))
    vendor_files.append(("vendor-capabilities.csv", agg_rows))
    # header-only aggregate file is OK only when the descriptor declares a fit grid
    errs += check_aggregate_vendor_capabilities(agg_rows, vendor_fit)
    if vendor_fit:
        # the declared fit grid substitutes for the matrix -> it is gated too
        errs += check_vendor_fit(m, vendor_fit)
    for p in sorted(glob.glob(os.path.join(m, "vendor-capabilities-*.csv"))):
        name = os.path.basename(p)
        rows = load_csv(p)
        vendor_files.append((name, rows))
        errs += validate_vendor_rows(name, rows, single_slug=True)

    errs += validate_referential(use_cases, current, trace, identity, vendor_files)
    errs += check_no_legacy_token(current, identity)

    # provenance gate (theme F): control-ID registry + citations + data-provenance.
    # Config is cross-domain — always from <root>/matrix/config, not the data dir.
    cfg = os.path.join(root, "matrix", "config")
    registry = load_yaml(os.path.join(cfg, "control-id-registry.yaml"))
    semantics = load_yaml(os.path.join(cfg, "control-semantics.yaml"))
    provenance = load_yaml(os.path.join(cfg, "data-provenance.yaml"))
    ownership = load_yaml(os.path.join(cfg, "vendor-ownership.yaml"))
    errs += check_control_id_registry(trace, registry)
    errs += check_control_semantics(trace, semantics)
    errs += check_ownership_sources(ownership)
    # M2 cross-domain identity spine: registry well-formed (mapping gate added in validate_all
    # once the spine_id column is present on the catalogs).
    spine = identity_spine.load_spine(cfg)
    errs += check_identity_spine_registry(spine)
    errs += check_identity_spine_mapping(identity, spine)
    for name, rows in vendor_files:
        errs += check_provider_claims_cited(name, rows)
    # H6: the aggregate must stay in sync with the per-vendor files it denormalises.
    per_vendor = [(n, r) for n, r in vendor_files if n != "vendor-capabilities.csv"]
    errs += check_aggregate_vendor_consistency(agg_rows, per_vendor)
    errs += check_data_provenance(trace, provenance)
    errs += check_data_currency(provenance)

    # evidence-pack gate: only runs when the domain ships an evidence catalog.
    catalog_path = os.path.join(m, "evidence-catalog.csv")
    catalog = load_csv(catalog_path) if os.path.exists(catalog_path) else None
    if catalog is not None:
        errs += check_evidence_packs(trace, catalog)

    # H1a citation-key resolution gate: every used citation key must resolve to
    # a bib entry (or be a documented sentinel). Bib is cross-domain: <root>/meta.
    cited_files = [("use-cases.csv", use_cases), ("current-state.csv", current),
                   ("regulatory-trace.csv", trace), ("identity-catalog.csv", identity)]
    cited_files += vendor_files
    # a descriptor-declared vendor-fit grid (matrix-less domains, e.g. IGA's
    # iga-vendor-fit.csv) carries its own citation_keys — it MUST be resolved too,
    # else its keys escape the gate (it is not part of vendor_files).
    if vendor_fit:
        fit_path = os.path.join(m, vendor_fit)
        if os.path.exists(fit_path):
            cited_files.append((vendor_fit, load_csv(fit_path)))
    if catalog is not None:
        cited_files.append(("evidence-catalog.csv", catalog))
    errs += check_citation_keys_resolve(os.path.join(root, "meta", "citations.bib"),
                                        cited_files)
    return errs


def main(argv=None):
    ap = argparse.ArgumentParser(description="Validate the matrix CSV data contracts.")
    ap.add_argument("--root", default=".", help="repo root (default: cwd)")
    ap.add_argument("--data-dir", default=None,
                    help="domain data dir holding the five CSVs (default: the secrets "
                         "domain, resolved via its descriptor → matrix/domains/secrets)")
    args = ap.parse_args(argv)
    violations = validate_all(args.root, data_dir=args.data_dir)
    for v in violations:
        print(v)
    if violations:
        print(f"\n{len(violations)} violation(s) found.")
        return 1
    print("All CSV data contracts valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
