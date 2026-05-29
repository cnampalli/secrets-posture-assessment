# WS-2 Selectable Regulatory Overlay — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace hardcoded, FI/APRA-flavoured framework labels, vendor-residency data, and framework scoping in `matrix/build_matrix_viewer.py` with declarative YAML config — a 4-preset library plus an industry-tunable residency weighting knob — without changing the default (no-config) output.

**Architecture:** Two new pure, unit-testable modules (`engagement_config.py`, `overlay.py`) own all new logic; the 956-line `build_matrix_viewer.py` monolith gets minimal wiring (argparse, config resolution, scoped framework list, weight-aware sort key, a `framework_selection` metadata block, and a test-only `--emit-data` hook). Data migration (framework labels, vendor residency) is done by AST-extraction from the current source — never hand-copied — and guarded by JSON snapshot tests. A no-config run is byte-faithful to today's report (golden regression).

**Tech Stack:** Python 3 (stdlib + PyYAML), pytest 8.

---

## Design references

- Spec: `docs/superpowers/specs/2026-05-29-ws2-regulatory-overlay-design.md`
- Available framework slugs (the ONLY valid scope values), from `matrix/regulatory-trace.csv`:
  `essential-8`, `cisa-ztmm-v2`, `apra-cps-234`, `apra-cps-230`, `apra-cpg-234`, `asd-ism`, `mitre-attack`
- Current hardcoded structures in `matrix/build_matrix_viewer.py`:
  - `FRAMEWORK_LABELS` — dict slug → `(label, subtitle)` tuple (~L179)
  - `VENDOR_RESIDENCY` — dict slug → `{residency, irap, note}` (~L71)
  - `RES_ORDER = {"AU-RESIDENT": 0, "CONDITIONAL": 1, "SAAS-ONLY": 2}` (~L257)
  - `fw_order` — derived from `regulatory-trace.csv` row order (~L188)
  - vendor sorts keyed `(RES_ORDER[res], -native, ...)` (~L290–295)
  - primary selection: `_irap_au = [v ... res=="AU-RESIDENT" and irap=="YES"]` (~L299–300)
  - `REGDATA` dict assembled ~L223; `RECDATA` assembled later; both injected into HTML via `/*__REGDATA__*/{}` and `/*__RECDATA__*/{}` markers (~L944–945)

## File structure (created / modified)

| Path | Status | Responsibility |
|---|---|---|
| `requirements.txt` | Create | Declares `PyYAML`. |
| `matrix/engagement_config.py` | Create | YAML loading, preset+override+CLI resolution, slug validation, `EngagementConfig`. Sole owner of YAML parsing. |
| `matrix/overlay.py` | Create | Pure scoping/ordering helpers + config-file loaders (framework labels, vendor residency). |
| `matrix/config/frameworks.yaml` | Create (generated) | Externalized `FRAMEWORK_LABELS`. |
| `matrix/config/vendor-residency.yaml` | Create (generated) | Externalized `VENDOR_RESIDENCY`. |
| `matrix/config/presets/financial.yaml` | Create | APRA×3 + E8 baseline + ZTMM overlay; weight high, IRAP required. |
| `matrix/config/presets/government.yaml` | Create | ISM + E8 baseline; weight high, IRAP required. |
| `matrix/config/presets/retail.yaml` | Create | E8 only; weight low, IRAP not required. |
| `matrix/config/presets/baseline.yaml` | Create | E8 only; weight medium, IRAP not required. |
| `matrix/config/engagement.example.yaml` | Create | Documented engagement template. |
| `matrix/config/_generate_from_source.py` | Create | One-shot AST extractor → writes the two config YAMLs + two JSON snapshots. Kept as provenance. |
| `matrix/build_matrix_viewer.py` | Modify | Wire config in; scope frameworks; weight-aware sort; `framework_selection`; `--emit-data`. |
| `tests/__init__.py` | Create (if absent) | Make `tests` a package. |
| `tests/fixtures/framework-labels.snapshot.json` | Create (generated) | Frozen truth for label migration. |
| `tests/fixtures/vendor-residency.snapshot.json` | Create (generated) | Frozen truth for residency migration. |
| `tests/fixtures/data-baseline.json` | Create (generated) | Frozen `{REGDATA, RECDATA}` from the UNMODIFIED engine. |
| `tests/test_overlay.py` | Create | Unit tests for `overlay.py`. |
| `tests/test_engagement_config.py` | Create | Unit tests for `engagement_config.py`. |
| `tests/test_engine_integration.py` | Create | Subprocess golden-regression + scoping + weighting tests. |
| `docs/adr/ADR-009-regulatory-overlay-config.md` | Create | Records externalization + PyYAML tradeoff. |
| `meta/IMPROVEMENT-BACKLOG.md` | Modify | Mark WS-2 ✅; record deferred data gap. |

**All commands below assume CWD = repo root** (`/Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers`).

---

## Task 0: Dependency + freeze the golden baseline

**Files:**
- Create: `requirements.txt`, `tests/__init__.py`, `tests/fixtures/data-baseline.json`

- [ ] **Step 1: Create `requirements.txt`**

```
PyYAML>=6.0
```

- [ ] **Step 2: Install + verify PyYAML and pytest are importable**

Run: `pip install -r requirements.txt && python3 -c "import yaml, pytest; print('ok', yaml.__version__)"`
Expected: `ok 6.x`

- [ ] **Step 3: Create `tests/__init__.py`** (empty file)

```python
```

- [ ] **Step 4: Capture the frozen baseline from the UNMODIFIED engine**

This runs today's engine, then extracts the two embedded JSON bundles from the generated HTML using a balanced-brace scan. Run this BEFORE any engine edit.

Run:
```bash
python3 matrix/build_matrix_viewer.py
python3 - <<'PY'
import json, re, pathlib
html = pathlib.Path("matrix/matrix-viewer.html").read_text(encoding="utf-8")

def extract(varname):
    # find "const <varname> = {" and walk balanced braces
    m = re.search(r"const\s+" + re.escape(varname) + r"\s*=\s*", html)
    i = html.index("{", m.end())
    depth, j, instr, esc = 0, i, False, False
    while j < len(html):
        c = html[j]
        if instr:
            if esc: esc = False
            elif c == "\\": esc = True
            elif c == '"': instr = False
        else:
            if c == '"': instr = True
            elif c == "{": depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    return json.loads(html[i:j+1])
        j += 1
    raise ValueError(varname)

pathlib.Path("tests/fixtures").mkdir(parents=True, exist_ok=True)
baseline = {"REGDATA": extract("REGDATA"), "RECDATA": extract("RECDATA")}
pathlib.Path("tests/fixtures/data-baseline.json").write_text(
    json.dumps(baseline, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
print("frameworks:", [f["slug"] for f in baseline["REGDATA"]["frameworks"]])
print("recdata keys:", sorted(baseline["RECDATA"].keys()))
PY
```
Expected: prints all 7 framework slugs and RECDATA keys. `tests/fixtures/data-baseline.json` now exists.

- [ ] **Step 5: Commit**

```bash
git add requirements.txt tests/__init__.py tests/fixtures/data-baseline.json
git commit -m "chore(ws2): add PyYAML dep and freeze golden engine baseline"
```

---

## Task 1: Externalize FRAMEWORK_LABELS + VENDOR_RESIDENCY via AST generator

**Files:**
- Create: `matrix/config/_generate_from_source.py`
- Create (generated): `matrix/config/frameworks.yaml`, `matrix/config/vendor-residency.yaml`, `tests/fixtures/framework-labels.snapshot.json`, `tests/fixtures/vendor-residency.snapshot.json`

- [ ] **Step 1: Write the generator** (`matrix/config/_generate_from_source.py`)

```python
#!/usr/bin/env python3
"""One-shot provenance tool: extract FRAMEWORK_LABELS and VENDOR_RESIDENCY
literals from build_matrix_viewer.py via AST (no execution), and emit the
externalized YAML config plus frozen JSON snapshots for regression tests.

Run from repo root: python3 matrix/config/_generate_from_source.py
"""
import ast, json, os, pathlib
import yaml

HERE = pathlib.Path(__file__).resolve().parent          # matrix/config
MATRIX = HERE.parent                                     # matrix
SRC = MATRIX / "build_matrix_viewer.py"
FIX = MATRIX.parent / "tests" / "fixtures"


def extract_literal(name):
    tree = ast.parse(SRC.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == name for t in node.targets
        ):
            return ast.literal_eval(node.value)
    raise SystemExit(f"{name} not found in {SRC}")


def main():
    FIX.mkdir(parents=True, exist_ok=True)

    # FRAMEWORK_LABELS: {slug: (label, subtitle)} -> YAML {slug: {label, subtitle}}
    labels = extract_literal("FRAMEWORK_LABELS")
    labels_yaml = {slug: {"label": lab, "subtitle": sub} for slug, (lab, sub) in labels.items()}
    (HERE / "frameworks.yaml").write_text(
        yaml.safe_dump(labels_yaml, sort_keys=False, allow_unicode=True), encoding="utf-8")
    (FIX / "framework-labels.snapshot.json").write_text(
        json.dumps({k: list(v) for k, v in labels.items()}, ensure_ascii=False, indent=2),
        encoding="utf-8")

    # VENDOR_RESIDENCY: {slug: {residency, irap, note}} -> YAML 1:1
    residency = extract_literal("VENDOR_RESIDENCY")
    (HERE / "vendor-residency.yaml").write_text(
        yaml.safe_dump(residency, sort_keys=False, allow_unicode=True), encoding="utf-8")
    (FIX / "vendor-residency.snapshot.json").write_text(
        json.dumps(residency, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"frameworks.yaml: {len(labels_yaml)} entries")
    print(f"vendor-residency.yaml: {len(residency)} entries")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run the generator**

Run: `python3 matrix/config/_generate_from_source.py`
Expected: `frameworks.yaml: 7 entries` and `vendor-residency.yaml: 19 entries`. Four files now exist (2 YAML, 2 JSON snapshots).

- [ ] **Step 3: Sanity-check the YAML round-trips and matches source**

Run:
```bash
python3 - <<'PY'
import yaml, json
fl = yaml.safe_load(open("matrix/config/frameworks.yaml"))
snap = json.load(open("tests/fixtures/framework-labels.snapshot.json"))
assert set(fl) == set(snap), "framework slugs differ"
for s in fl:
    assert [fl[s]["label"], fl[s]["subtitle"]] == snap[s], s
vr = yaml.safe_load(open("matrix/config/vendor-residency.yaml"))
vsnap = json.load(open("tests/fixtures/vendor-residency.snapshot.json"))
assert vr == vsnap, "vendor residency differs"
print("OK: 7 labels, 19 residency entries faithful")
PY
```
Expected: `OK: 7 labels, 19 residency entries faithful`

- [ ] **Step 4: Commit**

```bash
git add matrix/config/_generate_from_source.py matrix/config/frameworks.yaml matrix/config/vendor-residency.yaml tests/fixtures/framework-labels.snapshot.json tests/fixtures/vendor-residency.snapshot.json
git commit -m "feat(ws2): externalize framework labels + vendor residency to YAML"
```

---

## Task 2: `overlay.py` — config loaders (TDD)

**Files:**
- Create: `matrix/overlay.py`
- Test: `tests/test_overlay.py`

- [ ] **Step 1: Write the failing test** (`tests/test_overlay.py`)

```python
import json, pathlib
import overlay

ROOT = pathlib.Path(__file__).resolve().parent.parent
CFG = ROOT / "matrix" / "config"
FIX = pathlib.Path(__file__).resolve().parent / "fixtures"


def test_load_framework_labels_matches_snapshot():
    snap = json.load(open(FIX / "framework-labels.snapshot.json"))
    labels = overlay.load_framework_labels(CFG / "frameworks.yaml")
    assert set(labels) == set(snap)
    for slug, (lab, sub) in labels.items():
        assert [lab, sub] == snap[slug]            # tuple shape preserved


def test_load_vendor_residency_matches_snapshot():
    snap = json.load(open(FIX / "vendor-residency.snapshot.json"))
    assert overlay.load_vendor_residency(CFG / "vendor-residency.yaml") == snap
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_overlay.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'overlay'`

- [ ] **Step 3: Write minimal implementation** (`matrix/overlay.py`)

```python
"""Pure scoping/ordering helpers + config-file loaders for the regulatory
overlay engine. No global state; safe to import from tests."""
import yaml

RES_RANK = {"AU-RESIDENT": 0, "CONDITIONAL": 1, "SAAS-ONLY": 2}


def _load_yaml(path):
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def load_framework_labels(path):
    """Return {slug: (label, subtitle)} — tuple shape the engine expects."""
    raw = _load_yaml(path)
    return {slug: (d["label"], d["subtitle"]) for slug, d in raw.items()}


def load_vendor_residency(path):
    """Return {slug: {residency, irap, note}} verbatim."""
    return _load_yaml(path)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_overlay.py -v`
Expected: PASS (2 tests). Run with `PYTHONPATH=matrix` if `overlay` not found: `PYTHONPATH=matrix python3 -m pytest tests/test_overlay.py -v`

- [ ] **Step 5: Add a `conftest.py` so `matrix/` is importable**

Create `tests/conftest.py`:
```python
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "matrix"))
```

Run: `python3 -m pytest tests/test_overlay.py -v`
Expected: PASS without needing `PYTHONPATH`.

- [ ] **Step 6: Commit**

```bash
git add matrix/overlay.py tests/test_overlay.py tests/conftest.py
git commit -m "feat(ws2): overlay config loaders with snapshot regression tests"
```

---

## Task 3: `overlay.py` — residency sort key + primary selection (TDD)

**Files:**
- Modify: `matrix/overlay.py`, `tests/test_overlay.py`

- [ ] **Step 1: Write the failing tests** (append to `tests/test_overlay.py`)

```python
def test_vendor_sort_key_high_is_residency_first():
    # capability_keys are pre-negated (lower = better), as the engine builds them
    k = overlay.vendor_sort_key("high", "SAAS-ONLY", (-5, -2))
    assert k == (2, -5, -2)                         # res rank leads


def test_vendor_sort_key_off_drops_residency():
    assert overlay.vendor_sort_key("off", "SAAS-ONLY", (-5, -2)) == (-5, -2)


def test_vendor_sort_key_low_is_final_tiebreaker():
    assert overlay.vendor_sort_key("low", "CONDITIONAL", (-5, -2)) == (-5, -2, 1)


def test_vendor_sort_key_medium_after_primary_metric():
    assert overlay.vendor_sort_key("medium", "CONDITIONAL", (-5, -2)) == (-5, 1, -2)


def test_select_primary_gate_on_prefers_irap_au():
    vendors = [
        {"slug": "v-cap", "residency": "AU-RESIDENT", "irap": "NO"},
        {"slug": "v-irap", "residency": "AU-RESIDENT", "irap": "YES"},
    ]
    assert overlay.select_primary(vendors, irap_required=True)["slug"] == "v-irap"


def test_select_primary_gate_off_takes_capability_leader():
    vendors = [
        {"slug": "v-cap", "residency": "SAAS-ONLY", "irap": "NO"},
        {"slug": "v-irap", "residency": "AU-RESIDENT", "irap": "YES"},
    ]
    # list is already capability-sorted; gate off -> first wins
    assert overlay.select_primary(vendors, irap_required=False)["slug"] == "v-cap"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_overlay.py -k "sort_key or select_primary" -v`
Expected: FAIL — `AttributeError: module 'overlay' has no attribute 'vendor_sort_key'`

- [ ] **Step 3: Add implementation** (append to `matrix/overlay.py`)

```python
def vendor_sort_key(weight, residency, capability_keys):
    """Compose a sort key placing residency rank per the configured weight.

    capability_keys: tuple of already-negated capability metrics (lower=better),
    exactly as the engine builds them (e.g. (-secrets_native, -nhi_native)).
    """
    r = RES_RANK.get(residency, 9)
    if weight == "high":
        return (r,) + tuple(capability_keys)
    if weight == "medium":
        return (capability_keys[0], r) + tuple(capability_keys[1:])
    if weight == "low":
        return tuple(capability_keys) + (r,)
    if weight == "off":
        return tuple(capability_keys)
    raise ValueError(f"unknown residency weight: {weight!r}")


def select_primary(l1_secrets, irap_required):
    """Pick the primary secrets platform. Reproduces the engine's gate when
    irap_required=True; otherwise takes the capability leader (l1_secrets[0])."""
    if irap_required:
        irap_au = [v for v in l1_secrets
                   if v["residency"] == "AU-RESIDENT" and v["irap"] == "YES"]
        if irap_au:
            return irap_au[0]
        return next((v for v in l1_secrets if v["residency"] == "AU-RESIDENT"),
                    l1_secrets[0])
    return l1_secrets[0]
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_overlay.py -v`
Expected: PASS (all overlay tests).

- [ ] **Step 5: Commit**

```bash
git add matrix/overlay.py tests/test_overlay.py
git commit -m "feat(ws2): residency-weight sort key + irap-gated primary selection"
```

---

## Task 4: `overlay.scope_frameworks` (TDD)

**Files:**
- Modify: `matrix/overlay.py`, `tests/test_overlay.py`

- [ ] **Step 1: Write the failing tests** (append to `tests/test_overlay.py`)

```python
from types import SimpleNamespace

ALL = ["essential-8", "cisa-ztmm-v2", "apra-cps-234", "apra-cps-230",
       "apra-cpg-234", "asd-ism", "mitre-attack"]


def test_scope_default_returns_full_order_unchanged():
    cfg = SimpleNamespace(is_default=True, framework_scope=["essential-8"])
    assert overlay.scope_frameworks(ALL, cfg) == ALL


def test_scope_filters_and_preserves_source_order():
    cfg = SimpleNamespace(is_default=False,
                          framework_scope=["asd-ism", "essential-8"])
    # output keeps fw_order ordering, not config ordering
    assert overlay.scope_frameworks(ALL, cfg) == ["essential-8", "asd-ism"]
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_overlay.py -k scope -v`
Expected: FAIL — no attribute `scope_frameworks`.

- [ ] **Step 3: Add implementation** (append to `matrix/overlay.py`)

```python
def scope_frameworks(fw_order, cfg):
    """Filter fw_order to the configured scope, preserving fw_order's ordering.
    Default config (no preset/flags) passes through unchanged (regression anchor)."""
    if getattr(cfg, "is_default", False):
        return list(fw_order)
    scope = set(cfg.framework_scope)
    return [s for s in fw_order if s in scope]
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_overlay.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add matrix/overlay.py tests/test_overlay.py
git commit -m "feat(ws2): framework scoping helper (default passthrough)"
```

---

## Task 5: `engagement_config.py` — resolution + validation (TDD)

**Files:**
- Create: `matrix/engagement_config.py`
- Test: `tests/test_engagement_config.py`

- [ ] **Step 1: Write the failing tests** (`tests/test_engagement_config.py`)

```python
import pathlib
import engagement_config as ec

ROOT = pathlib.Path(__file__).resolve().parent.parent
PRESETS = ROOT / "matrix" / "config" / "presets"
AVAILABLE = ["essential-8", "cisa-ztmm-v2", "apra-cps-234", "apra-cps-230",
             "apra-cpg-234", "asd-ism", "mitre-attack"]


def test_default_is_all_frameworks_high_irap():
    cfg = ec.resolve(available=AVAILABLE)
    assert cfg.is_default is True
    assert cfg.residency_weight == "high"
    assert cfg.irap_required is True


def test_preset_financial_scope(tmp_path):
    cfg = ec.resolve(preset="financial", available=AVAILABLE, presets_dir=PRESETS)
    assert set(cfg.framework_scope) == {
        "apra-cps-234", "apra-cps-230", "apra-cpg-234", "essential-8", "cisa-ztmm-v2"}
    assert cfg.is_default is False
    assert cfg.residency_weight == "high"


def test_baseline_always_unioned(tmp_path):
    cfg_path = tmp_path / "e.yaml"
    cfg_path.write_text("primary: [asd-ism]\nresidency: {weight: high, irap_required: true}\n")
    cfg = ec.resolve(config_path=cfg_path, available=AVAILABLE, presets_dir=PRESETS)
    assert "essential-8" in cfg.framework_scope          # baseline default union'd


def test_cli_frameworks_override_preset():
    cfg = ec.resolve(preset="financial", cli_frameworks=["asd-ism"],
                     available=AVAILABLE, presets_dir=PRESETS)
    assert "asd-ism" in cfg.framework_scope
    assert "apra-cps-234" not in cfg.framework_scope     # CLI replaced primary


def test_unknown_slug_warned_and_skipped(tmp_path, capsys):
    cfg_path = tmp_path / "e.yaml"
    cfg_path.write_text("primary: [asd-ism, privacy-act]\n")
    cfg = ec.resolve(config_path=cfg_path, available=AVAILABLE, presets_dir=PRESETS)
    assert "privacy-act" not in cfg.framework_scope
    assert "privacy-act" in capsys.readouterr().err      # warned on stderr


def test_unknown_preset_raises():
    import pytest
    with pytest.raises(ec.ConfigError):
        ec.resolve(preset="nonprofit", available=AVAILABLE, presets_dir=PRESETS)


def test_bad_weight_raises(tmp_path):
    import pytest
    cfg_path = tmp_path / "e.yaml"
    cfg_path.write_text("primary: [asd-ism]\nresidency: {weight: extreme}\n")
    with pytest.raises(ec.ConfigError):
        ec.resolve(config_path=cfg_path, available=AVAILABLE, presets_dir=PRESETS)
```

> Note: this task depends on the presets existing. If executing strictly in order, create
> `matrix/config/presets/financial.yaml` (Task 6 content) before running these tests, or run
> Task 6 first. The recommended order is **Task 6 then Task 5**; they are listed 5→6 for
> narrative flow but have no other coupling.

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_engagement_config.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'engagement_config'`

- [ ] **Step 3: Write implementation** (`matrix/engagement_config.py`)

```python
"""Engagement config resolution for the regulatory overlay engine.

Resolves framework scope + residency tuning from (in precedence order):
CLI frameworks > inline engagement.yaml > named preset > built-in default.
Sole owner of YAML parsing for engagement/preset files."""
import sys

VALID_WEIGHTS = {"high", "medium", "low", "off"}
DEFAULT_BASELINE = ["essential-8"]      # always-on AU baseline (Privacy Act deferred)


class ConfigError(Exception):
    pass


def _require_yaml():
    try:
        import yaml
        return yaml
    except ImportError:
        raise ConfigError("PyYAML required — pip install -r requirements.txt")


def _load(path):
    yaml = _require_yaml()
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


class EngagementConfig:
    def __init__(self, selected, overlays, baseline, residency_weight,
                 irap_required, is_default):
        self.selected = selected
        self.overlays = overlays
        self.baseline = baseline
        self.residency_weight = residency_weight
        self.irap_required = irap_required
        self.is_default = is_default

    @property
    def framework_scope(self):
        seen, out = set(), []
        for s in list(self.selected) + list(self.overlays) + list(self.baseline):
            if s not in seen:
                seen.add(s)
                out.append(s)
        return out


def _validate_slugs(slugs, available, label):
    out = []
    for s in slugs:
        if s in available:
            out.append(s)
        else:
            print(f"WARN: {label} framework '{s}' not in regulatory-trace.csv "
                  f"— skipped (no control mappings yet).", file=sys.stderr)
    return out


def resolve(preset=None, config_path=None, cli_frameworks=None,
            available=None, presets_dir=None):
    available = list(available or [])

    # No selection of any kind -> default = today's full-scope behaviour.
    if not preset and not config_path and not cli_frameworks:
        return EngagementConfig(
            selected=list(available), overlays=[], baseline=[],
            residency_weight="high", irap_required=True, is_default=True)

    data = {}
    if preset:
        ppath = (presets_dir / f"{preset}.yaml") if presets_dir else None
        if not ppath or not ppath.exists():
            raise ConfigError(f"unknown preset '{preset}'")
        data = _load(ppath)
    if config_path:
        data = {**data, **_load(config_path)}   # inline overrides preset

    selected = list(data.get("primary", []) or [])
    overlays = list(data.get("overlays", []) or [])
    baseline = list(data.get("baseline", DEFAULT_BASELINE) or DEFAULT_BASELINE)

    if cli_frameworks:                          # CLI overrides primary entirely
        selected = list(cli_frameworks)

    res = data.get("residency", {}) or {}
    weight = res.get("weight", "high")
    if weight not in VALID_WEIGHTS:
        raise ConfigError(f"residency.weight must be one of {sorted(VALID_WEIGHTS)}, "
                          f"got {weight!r}")
    irap_required = bool(res.get("irap_required", True))

    selected = _validate_slugs(selected, available, "primary")
    overlays = _validate_slugs(overlays, available, "overlay")
    baseline = _validate_slugs(baseline, available, "baseline")

    cfg = EngagementConfig(selected, overlays, baseline, weight,
                           irap_required, is_default=False)
    if not cfg.framework_scope:
        raise ConfigError("resulting framework scope is empty after validation")
    return cfg
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_engagement_config.py -v`
Expected: PASS (7 tests). (Requires Task 6 presets present.)

- [ ] **Step 5: Commit**

```bash
git add matrix/engagement_config.py tests/test_engagement_config.py
git commit -m "feat(ws2): engagement config resolution + slug validation"
```

---

## Task 6: Author preset library + example config

**Files:**
- Create: `matrix/config/presets/financial.yaml`, `government.yaml`, `retail.yaml`, `baseline.yaml`, `matrix/config/engagement.example.yaml`

> Execute this before Task 5's test run (see note in Task 5).

- [ ] **Step 1: `matrix/config/presets/financial.yaml`**

```yaml
# Financial institutions — APRA-regulated. Reproduces today's residency posture.
primary:   [apra-cps-234, apra-cps-230, apra-cpg-234]
overlays:  [cisa-ztmm-v2]
baseline:  [essential-8]            # always-on AU baseline
residency:
  weight: high                      # AU residency is the primary vendor sort key
  irap_required: true               # primary must be AU-resident AND IRAP-assessed
```

- [ ] **Step 2: `matrix/config/presets/government.yaml`**

```yaml
# Australian government — ISM baseline.
primary:   [asd-ism]
overlays:  [cisa-ztmm-v2]
baseline:  [essential-8]
residency:
  weight: high
  irap_required: true
```

- [ ] **Step 3: `matrix/config/presets/retail.yaml`**

```yaml
# Retail / commercial — Essential 8 baseline, residency a soft preference.
primary:   [essential-8]
overlays:  [mitre-attack]
baseline:  [essential-8]
residency:
  weight: low                       # residency only as a final tiebreaker
  irap_required: false              # no IRAP gate on the primary pick
```

- [ ] **Step 4: `matrix/config/presets/baseline.yaml`**

```yaml
# Generic AU baseline — Essential 8 only. Industry-neutral starting point.
primary:   [essential-8]
overlays:  []
baseline:  [essential-8]
residency:
  weight: medium
  irap_required: false
```

- [ ] **Step 5: `matrix/config/engagement.example.yaml`**

```yaml
# Copy to engagement.yaml and edit for a real engagement.
# Run: python3 matrix/build_matrix_viewer.py --config engagement.yaml
#
# Either name a preset as the base:
preset: financial
#
# ...and/or override individual keys inline (inline wins over preset):
# primary:   [apra-cps-234]          # frameworks the report scopes to
# overlays:  [cisa-ztmm-v2, mitre-attack]   # comparison frameworks shown alongside
# baseline:  [essential-8]           # always-on; union'd in regardless
# residency:
#   weight: high                     # high | medium | low | off
#   irap_required: true              # gate primary vendor on AU-resident + IRAP
#
# Valid framework slugs (must exist in matrix/regulatory-trace.csv):
#   essential-8, cisa-ztmm-v2, apra-cps-234, apra-cps-230, apra-cpg-234,
#   asd-ism, mitre-attack
# Frameworks NOT yet available (deferred to a future research workstream):
#   privacy-act, my-health-record, pspf, soci
```

- [ ] **Step 6: Validate presets parse and resolve**

Run:
```bash
python3 - <<'PY'
import pathlib, sys
sys.path.insert(0, "matrix")
import engagement_config as ec
P = pathlib.Path("matrix/config/presets")
AV = ["essential-8","cisa-ztmm-v2","apra-cps-234","apra-cps-230","apra-cpg-234","asd-ism","mitre-attack"]
for name in ["financial","government","retail","baseline"]:
    c = ec.resolve(preset=name, available=AV, presets_dir=P)
    print(name, "->", c.framework_scope, c.residency_weight, c.irap_required)
PY
```
Expected: each preset prints a non-empty scope (financial includes the 3 APRA + E8 + ZTMM; all include essential-8).

- [ ] **Step 7: Commit**

```bash
git add matrix/config/presets/ matrix/config/engagement.example.yaml
git commit -m "feat(ws2): add 4-preset library + documented engagement template"
```

---

## Task 7: Wire config into `build_matrix_viewer.py`

**Files:**
- Modify: `matrix/build_matrix_viewer.py`

All edits below are anchored to existing code (line numbers drift as you edit — match on the shown text).

- [ ] **Step 1: Add imports + argparse + config resolution near the top**

After the existing `from collections import defaultdict` line and the `HERE = ...` block (before `VENDOR_LAYER`), insert:

```python
import argparse
import engagement_config as _ec
import overlay as _ov

_CFGDIR = os.path.join(HERE, "config")

_ap = argparse.ArgumentParser(description="Build the secrets-management report.")
_ap.add_argument("--config", help="path to an engagement.yaml")
_ap.add_argument("--preset", help="named preset (financial|government|retail|baseline)")
_ap.add_argument("--frameworks", help="comma-separated framework slugs (overrides primary)")
_ap.add_argument("--emit-data", help="(test hook) also dump {REGDATA,RECDATA} JSON to this path")
_ARGS, _ = _ap.parse_known_args()
```

- [ ] **Step 2: Delete the hardcoded `VENDOR_RESIDENCY` literal, load from YAML instead**

Replace the entire `VENDOR_RESIDENCY = { ... }` block (slug → {residency,irap,note}) with:

```python
# AU data-residency / IRAP per vendor — externalized to config/vendor-residency.yaml (WS-2).
VENDOR_RESIDENCY = _ov.load_vendor_residency(os.path.join(_CFGDIR, "vendor-residency.yaml"))
```

- [ ] **Step 3: Delete the hardcoded `FRAMEWORK_LABELS` literal, load from YAML instead**

Replace the entire `FRAMEWORK_LABELS = { ... }` block with:

```python
# Framework labels — externalized to config/frameworks.yaml (WS-2).
FRAMEWORK_LABELS = _ov.load_framework_labels(os.path.join(_CFGDIR, "frameworks.yaml"))
```

- [ ] **Step 4: Resolve the engagement config right after `reg_rows` / `fw_order` are built**

Find the `fw_order, fw_seen = [], set()` loop that builds `fw_order` from `reg_rows`. Immediately AFTER that loop completes, insert:

```python
_available = list(dict.fromkeys(fw_order))     # the framework slugs present in the data
_cli_fw = [s.strip() for s in _ARGS.frameworks.split(",")] if _ARGS.frameworks else None
import pathlib as _pl
ENGAGEMENT = _ec.resolve(
    preset=_ARGS.preset,
    config_path=_ARGS.config,
    cli_frameworks=_cli_fw,
    available=_available,
    presets_dir=_pl.Path(_CFGDIR) / "presets",
)
fw_order = _ov.scope_frameworks(fw_order, ENGAGEMENT)
```

- [ ] **Step 5: Add `framework_selection` to `REGDATA`**

Find the `REGDATA = { ... }` assignment. Add a `framework_selection` key inside it (alongside `"frameworks"`, `"controls"`, etc.):

```python
    "framework_selection": {
        "selected": list(ENGAGEMENT.selected) if not ENGAGEMENT.is_default else list(_available),
        "overlays": list(ENGAGEMENT.overlays),
        "baseline": list(ENGAGEMENT.baseline) if not ENGAGEMENT.is_default else [],
        "available": list(_available),
    },
```

Note: `REGDATA["frameworks"]` already iterates `fw_order`, which is now scoped — so the controls cascade is automatically scoped too.

- [ ] **Step 6: Replace the three `RES_ORDER`-keyed sorts with the weight-aware key**

Find the three `sorted(...)` calls (`l1_secrets`, `pki_mim`, `l2_governance`). Replace their `key=lambda v: (RES_ORDER.get(v["residency"], 9), ...)` with `overlay.vendor_sort_key`:

```python
l1_secrets = sorted((_vendor_stat(s) for s in _l1),
                    key=lambda v: _ov.vendor_sort_key(
                        ENGAGEMENT.residency_weight, v["residency"],
                        (-v["secrets_native"], -v["nhi_native"])))
pki_mim = sorted((_vendor_stat(s) for s in _pki),
                 key=lambda v: _ov.vendor_sort_key(
                     ENGAGEMENT.residency_weight, v["residency"],
                     (-v["secrets_native"],)))
l2_governance = sorted((_vendor_stat(s) for s in _l2),
                       key=lambda v: _ov.vendor_sort_key(
                           ENGAGEMENT.residency_weight, v["residency"],
                           (-v["gov_native"], -v["nhi_native"])))
```

You may leave the `RES_ORDER = {...}` definition in place (now unused) or delete it; deleting is cleaner.

- [ ] **Step 7: Route primary selection through `overlay.select_primary`**

Replace the two lines:

```python
_irap_au = [v for v in l1_secrets if v["residency"] == "AU-RESIDENT" and v["irap"] == "YES"]
_primary = _irap_au[0] if _irap_au else next((v for v in l1_secrets if v["residency"] == "AU-RESIDENT"), l1_secrets[0])
```

with:

```python
_primary = _ov.select_primary(l1_secrets, ENGAGEMENT.irap_required)
```

- [ ] **Step 8: Add the `--emit-data` test hook just before the HTML write**

Find `with open(DST, "w", encoding="utf-8") as f:`. Immediately BEFORE it, insert:

```python
if _ARGS.emit_data:
    with open(_ARGS.emit_data, "w", encoding="utf-8") as _ef:
        json.dump({"REGDATA": REGDATA, "RECDATA": RECDATA}, _ef,
                  ensure_ascii=False, sort_keys=True)
```

- [ ] **Step 9: Verify the default run still works and is byte-faithful**

Run:
```bash
python3 matrix/build_matrix_viewer.py --emit-data /tmp/ws2-default.json
python3 - <<'PY'
import json
base = json.load(open("tests/fixtures/data-baseline.json"))
new = json.load(open("/tmp/ws2-default.json"))
assert [f["slug"] for f in base["REGDATA"]["frameworks"]] == \
       [f["slug"] for f in new["REGDATA"]["frameworks"]], "framework order changed!"
assert base["RECDATA"] == new["RECDATA"], "RECDATA (vendor order) changed!"
# REGDATA gains framework_selection; compare everything else
nb = {k: v for k, v in new["REGDATA"].items() if k != "framework_selection"}
assert nb == base["REGDATA"], "REGDATA changed beyond framework_selection!"
print("OK: default run byte-faithful to frozen baseline")
PY
```
Expected: `OK: default run byte-faithful to frozen baseline`

- [ ] **Step 10: Commit**

```bash
git add matrix/build_matrix_viewer.py
git commit -m "feat(ws2): wire engagement config into engine (scope + weight + metadata)"
```

---

## Task 8: Integration tests — golden regression, scoping, weighting (TDD)

**Files:**
- Create: `tests/test_engine_integration.py`

- [ ] **Step 1: Write the tests**

```python
import json, subprocess, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
ENGINE = ROOT / "matrix" / "build_matrix_viewer.py"
BASELINE = json.load(open(ROOT / "tests" / "fixtures" / "data-baseline.json"))


def _run(tmp_path, *args):
    out = tmp_path / "data.json"
    subprocess.run([sys.executable, str(ENGINE), "--emit-data", str(out), *args],
                   cwd=ROOT, check=True)
    return json.load(open(out))


def test_default_run_matches_frozen_baseline(tmp_path):
    new = _run(tmp_path)
    assert [f["slug"] for f in new["REGDATA"]["frameworks"]] == \
           [f["slug"] for f in BASELINE["REGDATA"]["frameworks"]]
    assert new["RECDATA"] == BASELINE["RECDATA"]


def test_financial_preset_scopes_frameworks(tmp_path):
    new = _run(tmp_path, "--preset", "financial")
    slugs = {f["slug"] for f in new["REGDATA"]["frameworks"]}
    assert slugs == {"apra-cps-234", "apra-cps-230", "apra-cpg-234",
                     "essential-8", "cisa-ztmm-v2"}
    assert "asd-ism" not in slugs and "mitre-attack" not in slugs


def test_government_preset_scopes_to_ism_and_e8(tmp_path):
    new = _run(tmp_path, "--preset", "government")
    slugs = {f["slug"] for f in new["REGDATA"]["frameworks"]}
    assert slugs == {"asd-ism", "essential-8", "cisa-ztmm-v2"}


def test_framework_selection_metadata_present(tmp_path):
    new = _run(tmp_path, "--preset", "financial")
    sel = new["REGDATA"]["framework_selection"]
    assert sel["baseline"] == ["essential-8"]
    assert set(sel["available"]) >= {"asd-ism", "mitre-attack"}   # full menu retained


def test_cli_frameworks_override(tmp_path):
    new = _run(tmp_path, "--frameworks", "asd-ism")
    slugs = {f["slug"] for f in new["REGDATA"]["frameworks"]}
    assert "asd-ism" in slugs and "apra-cps-234" not in slugs


def test_residency_weight_off_changes_vendor_order(tmp_path):
    cfg = tmp_path / "off.yaml"
    cfg.write_text("primary: [apra-cps-234]\nbaseline: [essential-8]\n"
                   "residency: {weight: off, irap_required: false}\n")
    new = _run(tmp_path, "--config", str(cfg))
    # capability-only order differs from the residency-first baseline order
    base_primary = BASELINE["RECDATA"]["top_picks"][0]["slug"]
    new_primary = new["RECDATA"]["top_picks"][0]["slug"]
    # at minimum the full L1 ordering must differ
    assert new["RECDATA"]["top_picks"] != BASELINE["RECDATA"]["top_picks"] \
        or new_primary != base_primary
```

> If `RECDATA` has no `top_picks` key, adjust the last test to read whatever key holds the
> ranked L1 vendor list (inspect `tests/fixtures/data-baseline.json` → `RECDATA` keys). The
> assertion only needs *some* ordered vendor list that residency weight affects.

- [ ] **Step 2: Run the full suite**

Run: `python3 -m pytest tests/ -v`
Expected: PASS — all overlay, config, and integration tests green.

- [ ] **Step 3: Commit**

```bash
git add tests/test_engine_integration.py
git commit -m "test(ws2): integration golden-regression + scoping + weighting"
```

---

## Task 9: ADR + backlog update + finalize

**Files:**
- Create: `docs/adr/ADR-009-regulatory-overlay-config.md`
- Modify: `meta/IMPROVEMENT-BACKLOG.md`

- [ ] **Step 1: Write ADR-009** (`docs/adr/ADR-009-regulatory-overlay-config.md`)

```markdown
# ADR-009: Selectable Regulatory Overlay via Externalized YAML Config

**Status:** Accepted
**Date:** 2026-05-29
**Workstream:** WS-2

## Context
The report engine (`matrix/build_matrix_viewer.py`) hardcoded framework labels,
per-vendor AU residency/IRAP data, and an implicit all-frameworks scope with
FI/APRA-flavoured, residency-first vendor ordering. This blocked reuse for
non-FI, non-APRA clients.

## Decision
Externalize framework labels and vendor residency to `matrix/config/*.yaml`.
Add an engagement config (preset + inline override + CLI) that scopes the report
to selected framework(s) + overlays over an always-on Essential 8 baseline, and a
residency `weight` (high|medium|low|off) + independent `irap_required` gate. A
no-config run reproduces the previous output exactly (golden regression test).
Ship 4 presets: financial, government, retail, baseline.

## Consequences
- (+) Industry-agnostic scoping with zero new research; WS-3 JS toggle enabled via
  `framework_selection.available` metadata.
- (−) Adds a PyYAML runtime dependency (`requirements.txt`), trading away
  bare-`python3` portability for human-editable config. Mitigated by a clear
  install-error message.
- Scope limited to the 7 frameworks in `regulatory-trace.csv`. Privacy Act,
  My Health Record, PSPF, SOCI (and a health preset) are deferred to a future
  new-research workstream; configs referencing them are warned and skipped.
```

- [ ] **Step 2: Mark WS-2 done in `meta/IMPROVEMENT-BACKLOG.md`**

Change the `### WS-2 — Selectable regulatory overlay (engine)` heading to append
`— ✅ DONE (2026-05-29, branch ws2-regulatory-overlay)` and add a one-line note under it:

```markdown
Delivered: config-driven framework scoping + 4 presets (financial/government/retail/baseline) +
residency weight/IRAP knobs in `matrix/config/`; engine wired in `build_matrix_viewer.py`;
golden no-config regression + integration tests. ADR-009. **Deferred:** Privacy Act / MyHR /
PSPF / SOCI control→UC mappings and a health preset require a new-research workstream.
```

- [ ] **Step 3: Run the full suite once more + a clean default build**

Run: `python3 -m pytest tests/ -v && python3 matrix/build_matrix_viewer.py`
Expected: all tests PASS; engine prints its normal `Wrote .../matrix-viewer.html` summary.

- [ ] **Step 4: Commit**

```bash
git add docs/adr/ADR-009-regulatory-overlay-config.md meta/IMPROVEMENT-BACKLOG.md
git commit -m "docs(ws2): ADR-009 + mark WS-2 done in improvement backlog"
```

- [ ] **Step 5: Push + open PR**

```bash
git push -u origin ws2-regulatory-overlay
gh pr create --title "WS-2: Selectable regulatory overlay (engine)" \
  --body "Externalizes framework labels + vendor residency to YAML; adds engagement config (preset/CLI/inline), 4-preset library, and industry-tunable residency weighting. No-config run is byte-faithful to the previous report (golden regression). Scoped to the 7 frameworks in regulatory-trace.csv; Privacy Act/MyHR/PSPF/SOCI deferred. ADR-009.

Spec: docs/superpowers/specs/2026-05-29-ws2-regulatory-overlay-design.md
Plan: docs/superpowers/plans/2026-05-29-ws2-regulatory-overlay.md"
```

---

## Self-review notes (author)

- **Spec coverage:** §4 architecture → Tasks 2–7; §5 components → all created; §6 schema/precedence → Task 5 + Task 6; §7 residency weighting → Task 3 + Task 7.6/7.7; §8 framework_selection → Task 7.5 + Task 8; §9 error handling → Task 5 tests (unknown preset/slug/weight, empty scope) + `_require_yaml`; §10 testing → Tasks 2–8; §11 PyYAML tradeoff → Task 0 + ADR-009.
- **Ordering caveat:** Task 6 (presets) must run before Task 5's test step — flagged inline.
- **Type consistency:** `EngagementConfig.framework_scope`, `.selected`, `.overlays`, `.baseline`, `.residency_weight`, `.irap_required`, `.is_default` used consistently across Tasks 4/5/7. `overlay.vendor_sort_key(weight, residency, capability_keys)` and `overlay.select_primary(l1_secrets, irap_required)` signatures match between Task 3 and Task 7.
- **Residency regression risk:** default weight `high` + `vendor_sort_key("high", res, caps)` reproduces `(RES_ORDER[res], *caps)` exactly; `select_primary(..., True)` reproduces the original gate — Task 7.9 + Task 8.1 assert byte-fidelity.
```
