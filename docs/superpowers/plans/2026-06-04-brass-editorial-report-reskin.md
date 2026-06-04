# Brass Editorial — Report Re-skin Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Re-skin the two Python-generated deliverables — the matrix viewer (`matrix/matrix-viewer.html`) and the executive summary (`presentation/exec-summary.html`) — to the Brass Editorial design language, sharing the SAME token values as the React app so all three deliverables read as one premium offline product.

**Architecture:** The canonical colour/type tokens already live once in `design/brass-editorial.tokens.json` → emitted to `design/brass-editorial.vars.css` (a `:root` light block + a `.dark` block) by Plan 1. We inject that file's contents into each report's `<style>` at build time via a new `brand_tokens.py` helper (mirroring the existing `brand_fonts.py`), then re-point each report's existing (indigo-era) local `:root` palette so its local token names alias the canonical Brass vars. Result: change a colour in `tokens.json` → re-emit → app **and** both reports update. Reports are light-only (no theme toggle), so the injected `.dark` block is inert but harmless. Fonts switch from Schibsted/Hanken to Fraunces/Inter/JetBrains Mono by swapping the woff2 files and `_FACES` in `brand_fonts.py`.

**Tech Stack:** Python 3 (stdlib `base64`, string token-replacement builds), pytest. Fonts: Fraunces / Inter / JetBrains Mono (OFL variable woff2, already downloaded to `app/src/assets/fonts/` by Plan 1). No new dependencies.

**Plan 3 of 3** (Foundation → Questionnaire → **Report re-skin**). Spec: `docs/superpowers/specs/2026-06-03-brass-editorial-react-uplift-design.md` §3.2, §4-C. Branch: `feat/brass-editorial-ui` (already checked out).

---

## Working-tree note (read before Task 1)

The report files are **currently in their indigo-round state in the working tree** (uncommitted edits — fully tokenized with `var(--…)`, indigo palette). **We keep that tokenization and only change the token VALUES + fonts.** Do **not** `git checkout --` these files; that would revert to the pre-indigo monolith and throw away the var() infrastructure this plan relies on. The net diff each commit produces (vs `HEAD`) is therefore "tokenized + Brass-skinned report files" — that is the intended change.

Files this plan touches:
- Modify: `brand_fonts.py` (font faces)
- Create: `brand_tokens.py`, `tests/test_brand_tokens.py`, `tests/test_brand_fonts.py`
- Create (copied): `assets/fonts/fraunces.woff2`, `assets/fonts/inter.woff2` (jetbrains-mono already present)
- Modify: `matrix/report-template.html` (add `/*__TOKENS__*/` marker; rewrite `:root` palette), `matrix/report_render.py` (inject tokens)
- Modify: `presentation/exec-summary-template.html` (add `/*__TOKENS__*/` marker), `presentation/build_exec_summary.py` (inject tokens), `presentation/exec-summary.css` (rewrite `:root` palette + print override)
- Regenerate: `tests/fixtures/report.snapshot.html`
- Modify (docstrings/asset license): `assets/fonts/LICENSES.md`

---

## Task 1: Swap brand fonts to Fraunces / Inter / JetBrains Mono

**Files:**
- Copy: `app/src/assets/fonts/fraunces.woff2` → `assets/fonts/fraunces.woff2`; `app/src/assets/fonts/inter.woff2` → `assets/fonts/inter.woff2`
- Modify: `brand_fonts.py:28-32` (`_FACES`), `brand_fonts.py:1-20` (docstring families)
- Create: `tests/test_brand_fonts.py`
- Modify: `assets/fonts/LICENSES.md`

- [ ] **Step 1: Copy the Brass woff2 files into the Python font dir**

The Plan-1 app already downloaded valid OFL woff2 binaries. Reuse them (do NOT re-fetch — keep it offline/deterministic). `jetbrains-mono` already exists under both names; standardise on the app's filenames by copying all three, then dropping the old indigo fonts.

Run:
```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
cp app/src/assets/fonts/fraunces.woff2 assets/fonts/fraunces.woff2
cp app/src/assets/fonts/inter.woff2    assets/fonts/inter.woff2
cp app/src/assets/fonts/jetbrains-mono.woff2 assets/fonts/jetbrains-mono.woff2
git rm --quiet assets/fonts/hanken-grotesk-latin-var.woff2 assets/fonts/schibsted-grotesk-latin-var.woff2 assets/fonts/jetbrains-mono-latin-var.woff2 2>/dev/null || rm -f assets/fonts/hanken-grotesk-latin-var.woff2 assets/fonts/schibsted-grotesk-latin-var.woff2 assets/fonts/jetbrains-mono-latin-var.woff2
ls -1 assets/fonts/
```
Expected: `assets/fonts/` lists exactly `fraunces.woff2`, `inter.woff2`, `jetbrains-mono.woff2`, `LICENSES.md`.

- [ ] **Step 2: Write the failing font test**

Create `tests/test_brand_fonts.py`:
```python
import re
import brand_fonts


def test_faces_are_the_brass_editorial_families():
    families = {family for family, _ in brand_fonts._FACES}
    assert families == {"Fraunces", "Inter", "JetBrains Mono"}


def test_fontface_css_embeds_three_base64_woff2():
    css = brand_fonts.fontface_css()
    # one @font-face per family, each a base64 woff2 data URI (fully offline)
    assert css.count("@font-face") == 3
    assert css.count("data:font/woff2;base64,") == 3
    for family in ("Fraunces", "Inter", "JetBrains Mono"):
        assert f"font-family:'{family}'" in css
    # no external URLs
    assert not re.search(r"https?://", css)
```

- [ ] **Step 3: Run it — verify it fails**

Run: `cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers && python3 -m pytest tests/test_brand_fonts.py -q`
Expected: FAIL — `families == {'Hanken Grotesk', 'Schibsted Grotesk', 'JetBrains Mono'}` ≠ expected.

- [ ] **Step 4: Update `_FACES` and the docstring**

In `brand_fonts.py`, replace the `_FACES` tuple (lines 28-32):
```python
# (CSS family name, woff2 filename) — variable fonts, full 100–900 weight axis.
_FACES = (
    ("Fraunces", "fraunces.woff2"),
    ("Inter", "inter.woff2"),
    ("JetBrains Mono", "jetbrains-mono.woff2"),
)
```
And update the docstring families list (lines 16-19) to:
```python
Families (variable, weight axis 100–900):
  - Inter            → UI / body
  - Fraunces         → display / headings (serif)
  - JetBrains Mono   → IDs, codes, metrics
```
Also change the docstring phrase `"Modern SaaS clean" type system` → `Brass Editorial type system`.

- [ ] **Step 5: Run it — verify it passes**

Run: `cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers && python3 -m pytest tests/test_brand_fonts.py -q`
Expected: PASS (2 tests).

- [ ] **Step 6: Update the font licenses note**

In `assets/fonts/LICENSES.md`, replace the family list so it reads (one line per family):
```markdown
- Fraunces — SIL Open Font License 1.1
- Inter — SIL Open Font License 1.1
- JetBrains Mono — SIL Open Font License 1.1
```

- [ ] **Step 7: Commit**

```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
git add brand_fonts.py tests/test_brand_fonts.py assets/fonts
git commit -m "feat: swap report brand fonts to Fraunces/Inter/JetBrains Mono"
```

---

## Task 2: Shared token-CSS helper (`brand_tokens.py`)

**Files:**
- Create: `brand_tokens.py`
- Create: `tests/test_brand_tokens.py`

- [ ] **Step 1: Write the failing test**

Create `tests/test_brand_tokens.py`:
```python
import re
import brand_tokens


def test_tokens_css_contains_canonical_root_and_dark():
    css = brand_tokens.tokens_css()
    assert ":root" in css and ".dark" in css


def test_tokens_css_carries_brass_accent_and_fonts():
    css = brand_tokens.tokens_css()
    assert "--accent: #9a7b32;" in css          # light brass
    assert "--accent: #d6b25a;" in css          # dark brass
    assert "--font-display: 'Fraunces'" in css
    assert "--font-body: 'Inter'" in css
    assert "--font-mono: 'JetBrains Mono'" in css


def test_tokens_css_is_offline():
    assert not re.search(r"https?://", brand_tokens.tokens_css())
```

- [ ] **Step 2: Run it — verify it fails**

Run: `cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers && python3 -m pytest tests/test_brand_tokens.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'brand_tokens'`.

- [ ] **Step 3: Implement `brand_tokens.py`**

Create `brand_tokens.py` (repo root, next to `brand_fonts.py`):
```python
#!/usr/bin/env python3
"""Shared Brass Editorial design tokens for the generated reports.

The single source of truth for colour/type tokens is
``design/brass-editorial.tokens.json`` → emitted to
``design/brass-editorial.vars.css`` (a ``:root`` light block + a ``.dark``
block) by ``design/emit-tokens.mjs`` (Plan 1). The React app and these Python
reports both consume that one file, so a colour change in the tokens JSON
propagates everywhere after a single re-emit.

We inject the vars CSS into each report's ``<style>`` (via a ``/*__TOKENS__*/``
token) ahead of the report's own stylesheet, whose local ``:root`` then aliases
its token names to these canonical vars. Reports are light-only (no theme
toggle); the ``.dark`` block is inert but harmless. Reading a committed,
generated file keeps the build deterministic / byte-stable.
"""
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_VARS = os.path.join(_HERE, "design", "brass-editorial.vars.css")


def tokens_css():
    """Return the canonical Brass Editorial CSS-variable block (`:root` + `.dark`)."""
    with open(_VARS, encoding="utf-8") as fh:
        return fh.read()


if __name__ == "__main__":
    css = tokens_css()
    print(f"tokens_css(): {len(css)} chars from design/brass-editorial.vars.css")
```

- [ ] **Step 4: Run it — verify it passes**

Run: `cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers && python3 -m pytest tests/test_brand_tokens.py -q`
Expected: PASS (3 tests).

> If `test_tokens_css_carries_brass_accent_and_fonts` fails because the vars file is stale, regenerate it first: `node design/emit-tokens.mjs` (it must already contain the brass values shown in `design/brass-editorial.vars.css`; Plan 1 emitted them).

- [ ] **Step 5: Commit**

```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
git add brand_tokens.py tests/test_brand_tokens.py
git commit -m "feat: brand_tokens.py — inject canonical Brass tokens into reports"
```

---

## Task 3: Re-skin the matrix viewer

The matrix report `<style>` already uses `var(--…)` everywhere (228 uses). We (a) inject the canonical tokens via a new `/*__TOKENS__*/` marker, (b) rewrite the report's local `:root` (currently `matrix/report-template.html:10-32`) so its local names alias the canonical Brass vars + define report-only tokens (layer/vendor hues, shadows, radii) with warm Brass-aligned values, (c) delete local font/colour lines whose names collide with canonical vars so the canonical values flow through.

**Files:**
- Modify: `matrix/report-template.html` (add marker after `/*__FONTS__*/`; replace `:root` palette)
- Modify: `matrix/report_render.py` (inject tokens)

- [ ] **Step 1: Add the `/*__TOKENS__*/` marker to the template `<style>`**

In `matrix/report-template.html`, the `<style>` opens with `/*__FONTS__*/` on line 8. Insert a new line immediately after it (before the `:root{` on line ~10):
```html
/*__FONTS__*/
/*__TOKENS__*/
```
So the order in the built file is: @font-face rules → canonical `:root`/`.dark` Brass vars → the report's own stylesheet (including its aliasing `:root`).

- [ ] **Step 2: Wire the injection in `report_render.py`**

In `matrix/report_render.py`, add a `brand_tokens` import next to `brand_fonts` (after line 15):
```python
import brand_fonts
import brand_tokens
```
Then in `render()`, add the tokens replacement immediately after the `/*__FONTS__*/` replace (line 30):
```python
    return (load_template()
            .replace("/*__FONTS__*/", brand_fonts.fontface_css())
            .replace("/*__TOKENS__*/", brand_tokens.tokens_css())
            .replace("/*__DATA__*/[]", json.dumps(model["ranked"], ensure_ascii=False))
```
(leave the rest of the replace chain unchanged.)

- [ ] **Step 3: Replace the report's local `:root` palette**

In `matrix/report-template.html`, replace the **entire** local `:root{ … }` block (the indigo palette, lines ~10-32 — fonts, bg/ink/border, accent, layer/vendor hues, states, radii, shadows, ease) with the block below. This **aliases** local names to the injected canonical Brass vars and re-tunes report-only hues to the warm Editorial palette. Delete the old font-family `--font-display/body/mono` lines entirely (the canonical block already defines them as Fraunces/Inter/JetBrains Mono):
```css
  :root{
    /* fonts: --font-display/body/mono come from the injected canonical block */

    /* surfaces / ink / lines — alias to canonical Brass tokens */
    --bg-subtle:var(--bg2);--surface:var(--card);--surface-2:var(--bg2);
    --fg:var(--ink);--ink-2:var(--ink2);

    /* brass accent */
    --accent-hover:#856a2b;--accent-tint:var(--accent-soft);--accent-tint-2:#ece0c0;
    --accent-border:var(--accent-bd);--on-accent:var(--accent-fg);

    /* vendor stack layers (decorative, warm) */
    --l0:#9a7b32;--l1:#475069;--l2:#2f6b4f;

    /* vendor types */
    --native:var(--met);--native-tint:var(--met-soft);
    --addon:var(--partial);--addon-tint:var(--partial-soft);
    --partner:#7a4ea8;--partner-tint:#efe7f4;

    /* semantic state tints/ink (base hues come from the canonical block) */
    --gap-tint:var(--gap-soft);--gap-ink:#7e2626;
    --na-tint:var(--na-soft);
    --met-tint:var(--met-soft);--met-ink:#245a41;
    --partial-tint:var(--partial-soft);--partial-ink:#7c5418;
    --pending-tint:var(--pending-soft);--pending-ink:#3a4154;

    /* radii — alias to the canonical scale */
    --r-xs:var(--radius-xs);--r-sm:var(--radius-sm);--r-md:var(--radius-md);
    --r-lg:var(--radius-lg);--r-pill:var(--radius-pill);

    /* warm-tinted shadows + motion */
    --shadow-xs:0 1px 2px rgba(35,31,26,.06);
    --shadow-sm:0 1px 3px rgba(35,31,26,.07),0 1px 2px rgba(35,31,26,.04);
    --shadow-md:0 6px 16px -6px rgba(35,31,26,.14),0 2px 6px -4px rgba(35,31,26,.08);
    --shadow-lg:0 16px 40px -12px rgba(35,31,26,.20),0 6px 16px -10px rgba(35,31,26,.12);
    --ease:cubic-bezier(.22,.61,.36,1);
  }
```
> Note: `--bg`, `--card`, `--ink`, `--muted`, `--faint`, `--border`, `--border-strong`, `--accent`, `--met`, `--partial`, `--gap`, `--pending`, `--na` are **deliberately not redefined here** — they come straight from the injected canonical block (redefining them as `var(--bg)` etc. would be an invalid self-reference). Verify none remain in the local `:root` after the replace.

- [ ] **Step 4: Sweep the remaining raw hex literals**

The body rules still contain ~75 raw hex literals; most are intentional `color:#fff` on solid-colour chips/pills/bars (legible on Brass + state colours — leave them). Re-point only the two **structural pinkish error-border** literals to a warm token:

Run to find them: `cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers && grep -n "#f1cccc" matrix/report-template.html`
For each match (the `.placeholder`/warning border on ~line 40 and the `.tag-internal` border on ~line 98), replace `#f1cccc` with `var(--gap-soft)`.

Then confirm nothing else needs attention: `grep -noE "#[0-9a-fA-F]{3,8}" matrix/report-template.html | grep -viE "#fff|#ffffff" | sort -u` — expect only intentional decorative values (review the short list; map any obvious indigo leftover like `#3a56d4`, `#17212e`, `#f5f7fb` to the matching token if present in a body rule, though these should already live only in the now-replaced `:root`).

- [ ] **Step 5: Build the report and eyeball the head**

Run:
```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
python3 matrix/build_matrix_viewer.py
```
Expected: `Wrote …/matrix/matrix-viewer.html (… bytes)` plus the ranked/UC/NHI summary lines.

Verify tokens + fonts are inlined and no externals leaked:
```bash
grep -c "data:font/woff2;base64," matrix/matrix-viewer.html   # expect 3
grep -c -- "--accent: #9a7b32;" matrix/matrix-viewer.html      # expect >=1 (canonical injected)
grep -oE "(src|href)=\"https?://[^\"]+" matrix/matrix-viewer.html | head  # expect empty
```
Expected: `3`, `1` (or more), and no external-URL lines.

- [ ] **Step 6: Commit**

```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
git add matrix/report-template.html matrix/report_render.py matrix/matrix-viewer.html
git commit -m "feat: re-skin matrix viewer to Brass Editorial via shared tokens"
```

---

## Task 4: Re-skin the executive summary

`presentation/exec-summary.css` is fully tokenized (157 `var()` uses; local `:root` at lines 11-62; a print `:root` override at ~735). Same approach: inject canonical tokens ahead of the css, then alias the local `:root` (and the print override) to the Brass vars. The exec template's `<style>` is `/*__FONTS__*/\n/*__CSS__*/`; we add a `/*__TOKENS__*/` token between them and inject in `build()`.

**Files:**
- Modify: `presentation/exec-summary-template.html` (add marker)
- Modify: `presentation/build_exec_summary.py` (TOKENS tuple + inject + build)
- Modify: `presentation/exec-summary.css` (rewrite `:root` + print override)

- [ ] **Step 1: Add the `/*__TOKENS__*/` marker to the exec template**

In `presentation/exec-summary-template.html`, change the `<style>` body (lines 7-10) to:
```html
<style>
/*__FONTS__*/
/*__TOKENS__*/
/*__CSS__*/
</style>
```

- [ ] **Step 2: Wire the injection in `build_exec_summary.py`**

In `presentation/build_exec_summary.py`:

(a) Add `/*__TOKENS__*/` to the `TOKENS` tuple (line 24):
```python
TOKENS = ("/*__FONTS__*/", "/*__TOKENS__*/", "/*__CSS__*/", "/*__DATA__*/null", "/*__APP__*/")
```

(b) Update `inject()` to accept + replace tokens (lines 37-46):
```python
def inject(template, css, data, app, fonts="", tokens=""):
    """Replace the injection tokens; raise if any is missing."""
    for tok in TOKENS:
        if tok not in template:
            raise ExecSummaryError(f"template missing injection token: {tok}")
    return (template
            .replace("/*__FONTS__*/", fonts)
            .replace("/*__TOKENS__*/", tokens)
            .replace("/*__CSS__*/", css)
            .replace("/*__DATA__*/null", json.dumps(data, ensure_ascii=False))
            .replace("/*__APP__*/", app))
```

(c) Import `brand_tokens` next to `brand_fonts` (line 21):
```python
import brand_fonts
import brand_tokens
```

(d) Pass tokens in `build()` (line 74):
```python
    html = inject(template, css, data, app,
                  fonts=brand_fonts.fontface_css(), tokens=brand_tokens.tokens_css())
```

- [ ] **Step 3: Update the existing inject tests for the new signature**

The existing `tests/test_exec_summary.py::test_inject_replaces_tokens` builds its own template string and must include the new token, and `test_inject_missing_token_raises` already expects a raise. Update `test_inject_replaces_tokens` (lines 19-27):
```python
def test_inject_replaces_tokens():
    tmpl = ("<style>/*__FONTS__*/\n/*__TOKENS__*/\n/*__CSS__*/</style>"
            "<script>window.__EXEC_DATA__ = /*__DATA__*/null;</script><script>/*__APP__*/</script>")
    out = es.inject(tmpl, "BODY{}", {"a": 1}, "console.log(1)",
                    fonts="@font-face{}", tokens=":root{--accent:#9a7b32}")
    assert "BODY{}" in out
    assert "@font-face{}" in out
    assert "--accent:#9a7b32" in out
    assert "/*__FONTS__*/" not in out and "/*__TOKENS__*/" not in out
    assert '"a": 1' in out or '"a":1' in out
    assert "/*__DATA__*/null" not in out
    assert "console.log(1)" in out
```

- [ ] **Step 4: Run the inject tests — verify they fail (template marker not yet in real template is fine; these use inline templates)**

Run: `cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers && python3 -m pytest tests/test_exec_summary.py::test_inject_replaces_tokens tests/test_exec_summary.py::test_inject_missing_token_raises -q`
Expected: PASS once Steps 1-3 are applied (the inline template now carries `/*__TOKENS__*/`). If you run before editing `build_exec_summary.py`, it FAILs on the unknown `tokens=` kwarg — that confirms the new signature is required.

- [ ] **Step 5: Rewrite the exec `:root` palette to alias canonical vars**

In `presentation/exec-summary.css`, replace the local `:root{ … }` block (lines ~11-62) with the block below. Local names that **collide** with canonical (`--bg`, `--ink`, `--muted`, `--faint`, `--met`, `--partial`, `--gap`, `--pending`) are **omitted** (they flow through from the injected canonical block); everything else aliases or re-tunes to warm values:
```css
:root{
  /* surfaces (--bg, --ink, --muted, --faint come from the injected canonical block) */
  --bg-elev:   var(--bg2);
  --bg-card:   var(--card);
  --bg-card-2: var(--bg2);

  /* signal = Brass accent */
  --signal:     var(--accent);
  --signal-dim: #856a2b;

  /* state ink (base --met/--partial/--gap/--pending come from canonical) */
  --met-ink:     #245a41;
  --partial-ink: #7c5418;
  --gap-ink:     #7e2626;
  --pending-ink: #3a4154;

  /* state soft tints — alias to canonical soft tokens */
  --met-soft:     var(--met-soft);
  --partial-soft: var(--partial-soft);
  --gap-soft:     var(--gap-soft);
  --pending-soft: var(--pending-soft);

  /* hairlines (warm) */
  --line: rgba(154,123,50,.22);
  --hair: rgba(35,31,26,.09);
  --hair-strong: rgba(35,31,26,.15);

  /* warm-tinted elevation */
  --shadow-sm: 0 1px 3px rgba(35,31,26,.07), 0 1px 2px rgba(35,31,26,.04);
  --shadow-md: 0 6px 16px -6px rgba(35,31,26,.14), 0 2px 6px -4px rgba(35,31,26,.08);
  --shadow-lg: 0 16px 40px -12px rgba(35,31,26,.20), 0 6px 16px -10px rgba(35,31,26,.12);

  /* type — alias to canonical font tokens */
  --disp: var(--font-display);
  --mono: var(--font-mono);
  --body: var(--font-body);

  /* layout / motion (unchanged from indigo round) */
  --gut: clamp(20px, 4.5vw, 64px);
  --stack: clamp(48px, 7vw, 104px);
  --radius: var(--radius-lg);
  --ease: cubic-bezier(.22,.61,.36,1);
}
```
> The four `--*-soft: var(--*-soft)` lines are **not** self-references: the right-hand `--met-soft` etc. resolve against the canonical block injected *before* this stylesheet, and CSS resolves `var()` against the cascaded value, so the local `--met-soft` takes the canonical value. (If a linter flags these, replace the RHS with the canonical hexes from `design/brass-editorial.vars.css`: `--met-soft:#eaf2ec;` etc. — same result.)

- [ ] **Step 6: Update the print `:root` override**

In `presentation/exec-summary.css` (the `@media print` block, local `:root` override at ~lines 735-741), the indigo high-contrast print values must become warm-ink equivalents. Replace those override lines with:
```css
    --ink:   #1a1612;
    --muted: #4a443c;
    --faint: #6f6a62;
    --bg-card: #ffffff;
    --hair: rgba(0,0,0,.14);
    --hair-strong: rgba(0,0,0,.24);
    --line: rgba(0,0,0,.3);
```
(Only the colour values change; keep the surrounding `@media print` rules intact.)

- [ ] **Step 7: Sweep remaining raw hex in exec-summary.css**

Run: `cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers && grep -noE "#[0-9a-fA-F]{3,8}" presentation/exec-summary.css | grep -viE "#fff|#ffffff|#000" | sort -t: -k2 -u`
Review the list: any remaining indigo signature literals (`#3a56d4`, `#2c43b4`, `#17212e`, `#f5f7fb`, `#eef1f7`) in body rules should be re-pointed to the matching token (`var(--signal)`, `var(--ink)`, `var(--bg)`, `var(--bg-elev)`); leave on-colour whites/blacks and decorative values.

- [ ] **Step 8: Build the exec summary + verify offline/print/fonts**

Run:
```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
python3 - <<'PY'
import csv, json, tempfile, pathlib, presentation.build_exec_summary as es
ROOT = pathlib.Path("matrix")
rows = list(csv.DictReader(open(ROOT/"current-state.csv", encoding="utf-8")))
rec = {"schema":"posture-assessment-record/v1","responses":{
  r["uc_id"]:{"proposed_state":r["current_state"],"final_state":r["current_state"],
              "rationale":r.get("gap_notes","")} for r in rows}}
p = pathlib.Path(tempfile.mkdtemp())/"rec.json"; p.write_text(json.dumps(rec))
es.build(str(p), out_path="presentation/exec-summary.html")
PY
grep -c "data:font/woff2;base64," presentation/exec-summary.html   # expect 3
grep -c -- "--accent: #9a7b32;" presentation/exec-summary.html      # expect >=1
grep -c "@media print" presentation/exec-summary.html               # expect >=1
grep -oE "(src|href)=\"https?://[^\"]+" presentation/exec-summary.html | head  # expect empty
```
Expected: `3`, `>=1`, `>=1`, and no external-URL lines.

- [ ] **Step 9: Commit**

```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
git add presentation/exec-summary-template.html presentation/build_exec_summary.py presentation/exec-summary.css tests/test_exec_summary.py presentation/exec-summary.html
git commit -m "feat: re-skin executive summary to Brass Editorial via shared tokens"
```

---

## Task 5: Regenerate the matrix snapshot + full pytest

The matrix snapshot test (`tests/test_report_render.py::test_default_report_is_byte_identical`) md5-compares a fresh `matrix/build_matrix_viewer.py` build against `tests/fixtures/report.snapshot.html`. The re-skin intentionally changes those bytes, so the frozen snapshot must be regenerated **once**, deliberately.

**Files:**
- Regenerate: `tests/fixtures/report.snapshot.html`

- [ ] **Step 1: Confirm the snapshot test currently fails (proves the re-skin changed output)**

Run: `cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers && python3 -m pytest tests/test_report_render.py -q`
Expected: FAIL — "report HTML changed vs frozen snapshot".

- [ ] **Step 2: Regenerate the frozen snapshot from the freshly built report**

Run:
```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
python3 matrix/build_matrix_viewer.py
cp matrix/matrix-viewer.html tests/fixtures/report.snapshot.html
```
Expected: build prints `Wrote …`; snapshot file overwritten.

- [ ] **Step 3: Run the full Python suite**

Run: `cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers && python3 -m pytest -q`
Expected: all tests PASS (the prior 112 + the 5 new font/token tests; snapshot now matches). If any test asserts a specific indigo colour or font name, update that assertion to the Brass value and note it in the commit.

- [ ] **Step 4: Commit**

```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
git add tests/fixtures/report.snapshot.html
git commit -m "test: regenerate matrix report snapshot for Brass Editorial re-skin"
```

---

## Task 6: Visual QA across all three deliverables + final verification

**Files:** none (verification only)

- [ ] **Step 1: Rebuild all three deliverables fresh**

Run:
```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
python3 matrix/build_matrix_viewer.py
# exec summary built in Task 4 Step 8 (presentation/exec-summary.html)
cd app && npm run build && cd ..
```
Expected: matrix + app builds succeed; `app/dist/index.html`, `matrix/matrix-viewer.html`, `presentation/exec-summary.html` all present.

- [ ] **Step 2: Screenshot the two reports (light) for cohesion check**

Run:
```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CHROME" --headless=new --disable-gpu --force-device-scale-factor=2 --window-size=1280,1600 \
  --screenshot=/tmp/brass-matrix.png "file://$PWD/matrix/matrix-viewer.html"
"$CHROME" --headless=new --disable-gpu --force-device-scale-factor=2 --window-size=1100,1600 \
  --screenshot=/tmp/brass-exec.png "file://$PWD/presentation/exec-summary.html"
```
Expected: two PNGs. Open them and confirm: warm paper background, Fraunces serif headings, JetBrains Mono IDs/metrics, Brass `#9A7B32` accents, warm semantic state colours (MET green / PARTIAL ochre / GAP claret / PENDING slate) — visually consistent with the app's Editorial Light theme.

- [ ] **Step 3: Print-path check for the exec summary**

Open `presentation/exec-summary.html` in a real browser, invoke Print preview, and confirm the `@media print` layout still renders cleanly (warm ink on white, no clipped sections). This is a manual visual confirmation.

- [ ] **Step 4: Final full verification**

Run:
```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
python3 -m pytest -q
cd app && npm test && npm run build:check && cd ..
```
Expected: Python suite green; app **28** tests green; `OK — single self-contained offline index.html`.

- [ ] **Step 5: Confirm no external URLs anywhere in the three built files**

Run:
```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
for f in matrix/matrix-viewer.html presentation/exec-summary.html app/dist/index.html; do
  echo "== $f =="; grep -oE "(src|href)=\"https?://[^\"]+" "$f" | head || echo "(none)"
done
```
Expected: no external-URL lines for any file (all assets inlined / offline).

- [ ] **Step 6: Commit any final rebuild artifacts**

```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
git add matrix/matrix-viewer.html presentation/exec-summary.html
git commit -m "chore: rebuild reports after Brass Editorial re-skin" --allow-empty
```

---

## Self-Review (completed by author)

- **Spec coverage (§3.2, §4-C):** font swap to Fraunces/Inter/JetBrains Mono (Task 1); reuse of `design/brass-editorial.vars.css` injected into report templates so reports share the app's tokens (Tasks 2-4); matrix + exec re-skinned (Tasks 3-4); JS-keyed classes + `/*__X__*/` markers preserved (we only touch `:root` + add a `/*__TOKENS__*/` marker — all `const DATA = /*__DATA__*/[]` style markers and class names are untouched); `@media print` path preserved + verified (Task 4 Step 6, Task 6 Step 3); snapshot regenerated intentionally (Task 5); pytest green + visual QA cohesion (Tasks 5-6). Spec's "single source of truth" satisfied — values live once in `tokens.json`.
- **Placeholder scan:** none — every code/CSS/command step shows complete content. The two raw-hex "sweep" steps (T3S4, T4S7) are deterministic grep-then-map instructions over a known, finite literal set, not vague "clean up" asks.
- **Type consistency:** the `/*__TOKENS__*/` marker name is identical in both templates, both builders, and `brand_tokens.tokens_css()`; `inject()`'s new `tokens=` kwarg matches its call site and the updated test; local→canonical alias names (`--signal`→`--accent`, `--disp`→`--font-display`, `--r-*`→`--radius-*`, `--bg-subtle`→`--bg2`, `--surface`→`--card`, `--fg`→`--ink`, `--ink-2`→`--ink2`) are consistent across the matrix and exec `:root` rewrites; collision tokens (`--bg/--ink/--muted/--faint/--met/--partial/--gap/--pending`) are omitted from both local `:root` blocks to avoid self-reference.

---

## Execution Handoff

This is the final plan of the trilogy. After it is green:
- Whole-branch review (`superpowers:requesting-code-review`) covering the app + the report re-skin.
- `superpowers:finishing-a-development-branch` — decide PR vs merge; **consult the user** about the superseded indigo working-tree edits they have been carrying intentionally (this plan converts the report files to Brass; confirm before discarding any remaining indigo-only artifacts like `questionnaire/questionnaire.html`).
