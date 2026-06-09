#!/usr/bin/env python3
"""Phase 3 — IGA scoping spike.

HYPOTHESES:
  A) The domain-agnostic questionnaire engine (questionnaire.rubric_loader + the
     archetype library) expresses IGA *process-maturity* use cases with ZERO engine
     changes — only new data.
  B) The vendor capability-matrix engine wants fine-grained per-UC NATIVE/ADD-ON
     coverage; the hybrid model's *light* per-area vendor-fit overlay does not map 1:1.
     That mismatch is the finding, not a bug.

Run: python3 spikes/iga/run_iga_spike.py
NOTE: spikes/iga/*.csv are ILLUSTRATIVE (spike only) — not a verified IGA assessment.
"""
import csv
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, ROOT)

from questionnaire import rubric_loader  # noqa: E402

METH = os.path.join(ROOT, "methodology")
AREAS = ["JML", "Certification", "SoD", "Role/Request"]


def banner():
    print("=" * 72)
    print("IGA SCOPING SPIKE — ILLUSTRATIVE DATA ONLY (not a vendor assessment)")
    print("=" * 72)


def probe_a():
    """Questionnaire/archetype reuse — must run clean."""
    print("\n[Probe A] questionnaire/archetype reuse")
    ucs = rubric_loader.load_rubric(METH, data_dir=HERE)
    assert len(ucs) == 11, f"expected 11 IGA use cases, got {len(ucs)}"
    for uc in ucs:
        assert uc["kind"] == "ladder", f"{uc['uc_id']} not a ladder"
        for q in uc["questions"]:
            assert "{" not in q["text"], f"{uc['uc_id']} {q['qid']} unfilled slot"
    spread = sorted({u["archetype"] for u in ucs})
    print(f"  OK {len(ucs)} IGA use cases resolved; archetypes exercised: {spread}")
    print("  OK no engine changes required — rubric_loader is domain-agnostic")
    return ucs


def probe_b():
    """Vendor overlay vs the capability-matrix engine — record the seam."""
    print("\n[Probe B] light vendor-fit overlay vs capability-matrix engine")
    rows = list(csv.DictReader(open(os.path.join(HERE, "iga-vendor-fit.csv"), encoding="utf-8")))
    by_vendor = defaultdict(dict)
    for r in rows:
        by_vendor[r["vendor"]][r["area"]] = r["fit"]
    print(f"  overlay shape: {len(by_vendor)} vendors x {len(AREAS)} process areas (coarse fit)")
    for v, areas in by_vendor.items():
        print(f"    {v}: " + ", ".join(f"{a}={areas.get(a, '-')}" for a in AREAS))
    print("  SEAM: capability-matrix wants per-UC NATIVE/ADD-ON + identity-catalog;")
    print("    the hybrid overlay is per-area + coarse and does NOT map 1:1.")
    print("    -> full Phase 3 needs a dedicated lightweight IGA vendor-fit view (see findings).")


if __name__ == "__main__":
    banner()
    probe_a()
    probe_b()
    print("\nDONE — see spikes/iga/SPIKE-FINDINGS.md for the verdict.")
