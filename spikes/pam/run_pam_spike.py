#!/usr/bin/env python3
"""Phase 0.5 — PAM domain spike.

HYPOTHESIS: the Phase 0 analytic core (resilience, optimizer, vendor_intel,
compliance) and the report model-builders (report_logic.build_vendormix /
build_vendor_intel / build_compliance) are domain-agnostic — feeding them a PAM
dataset produces sensible vendor-mix / concentration / coverage output with ZERO
changes to any matrix/*.py module. Only NEW DATA + a little config (SHORT,
anchors) should be required.

If this runs clean, the "shared engine + per-domain model" abstraction holds and
Phase 1 (generalising the I/O loader + VENDOR_LAYER + template) is green-lit.
If it needs module edits, that leak is the finding.

Run: python3 spikes/pam/run_pam_spike.py
NOTE: pam-*.csv coverage/maturity values are ILLUSTRATIVE (spike only), not a
verified PAM vendor assessment.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
MATRIX = os.path.join(ROOT, "matrix")
sys.path.insert(0, MATRIX)  # import the UNCHANGED Phase 0 modules

import compliance            # noqa: E402
import optimizer             # noqa: E402
import overlay               # noqa: E402
import report_io             # noqa: E402
import report_logic          # noqa: E402
import resilience            # noqa: E402
import vendor_intel          # noqa: E402

# --- load the PAM domain (new data only) ---
ranked = report_io.read_csv(HERE, "pam-vendor-capabilities.csv")
ucs = report_io.read_csv(HERE, "pam-use-cases.csv")
reg_rows = report_io.read_csv(HERE, "pam-regulatory-trace.csv")
anz = report_io.read_csv(HERE, "pam-current-state.csv")
ownership = overlay.load_vendor_ownership(os.path.join(MATRIX, "config", "vendor-ownership.yaml"))
labels = overlay.load_framework_labels(os.path.join(MATRIX, "config", "frameworks.yaml"))

SHORT = {"cyberark-pam": "CyberArk PAM", "delinea-secret-server": "Delinea",
         "beyondtrust": "BeyondTrust"}
ANCHORS = ["cyberark-pam", "delinea-secret-server", "beyondtrust"]


def line(c="-"):
    print(c * 64)


print("PHASE 0.5 — PAM DOMAIN SPIKE  (analytic core on a non-secrets domain)")
line("=")
print(f"loaded: {len(ranked)} vendor rows · {len(ucs)} use cases · "
      f"{len({r['vendor_slug'] for r in ranked})} vendors · {len(reg_rows)} control rows")

# 1. resilience-first vendor mix + white-space (optimizer C1/C3)
mix = report_logic.build_vendormix(ranked, ownership, ANCHORS, SHORT)
line()
print("VENDOR MIX (resilience-first cover):",
      " + ".join(c["name"] for c in mix["cover"]["chosen"]))
print(f"  covers {mix['cover']['covered_count']}/{mix['cover']['uc_total']} UCs NATIVE "
      f"across {mix['portfolio']['distinct_parents']} parents")
print("  white-space (no NATIVE provider):", mix["cover"]["white_space"])
print("  single-source UCs (by parent):", mix["single_source"])
print("  concentration:", [(c["name"], f"{c['share']*100:.0f}%") for c in mix["concentration"]])

# 2. vendor intelligence: best vendor per UC + head-to-head (B2/B3/B4)
vi = report_logic.build_vendor_intel(ranked, ucs, ANCHORS, SHORT)
line()
print("BEST VENDOR PER UC (top 4):")
for b in vi["best_per_uc"][:4]:
    print(f"  {b['uc']}  {b['vendor']:<13} {b['coverage']}/{b['maturity']}  (+{b['alternatives']} alts)")
print("  head-to-head P0 UCs:", vi["head_to_head"]["uc_ids"])

# 3. identity/privilege-control coverage indicator + gap-to-target (D3/D4)
cmp = report_logic.build_compliance(reg_rows, anz, labels)
line()
print("CONTROL COVERAGE INDICATOR:")
for f in cmp["frameworks"]:
    print(f"  {f['label']:<16} MET {f['met']}/{f['total']}  "
          f"(partial {f['partial']} · gap {f['gap']} · pending {f['pending']})")
print("  gap-to-target:", [g["code"] for g in cmp["gap_to_target"]])

# 4. complement (C4) — have an incumbent, what fills the most gaps
line()
for slug in ("delinea-secret-server", "beyondtrust"):
    rec = optimizer.complement(slug, ranked)
    if rec:
        print(f"COMPLEMENT: have {SHORT[slug]} -> add {SHORT.get(rec['add'], rec['add'])} "
              f"(+{rec['fills']} UCs); still open: {rec['still_open']}")

# --- spike assertions: the architecture must produce these, no module edits ---
line("=")
checks = {
    "white-space detected (UC-P-011)": "UC-P-011" in mix["cover"]["white_space"],
    "EPM single-sourced (UC-P-009)": "UC-P-009" in mix["single_source"],
    "best_per_uc covers all functional UCs": len(vi["best_per_uc"]) >= 10,
    "coverage indicator ran on PAM frameworks": bool(cmp["frameworks"]),
    "MET surfaced where assessed (UC-P-007/MFA)":
        any(f["met"] >= 1 for f in cmp["frameworks"]),
}
for name, ok in checks.items():
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
verdict = all(checks.values())
print()
print("SPIKE VERDICT:", "ABSTRACTION HOLDS — 0 module changes, PAM ran on the Phase 0 core."
      if verdict else "LEAK FOUND — see failed checks.")
sys.exit(0 if verdict else 1)
