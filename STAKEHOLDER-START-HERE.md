# XYZ Secrets-Management — PRD v0.1 (start here)

**INTERNAL — prepared for a major AU Tier-1 FI (XYZ). Do not distribute
externally (open question O2).**

## What's in this package

| File | What it is | Who it's for |
|---|---|---|
| **XYZ-Secrets-Report.html** | Self-contained interactive report. **Double-click to open in any browser** — no install, works offline. | Everyone — start here |
| `PRD/PRD-FI-v0.1.md` | The full written PRD (20 sections). | Architecture / deep readers |
| `PRD/adrs/` | 7 architecture decision records. | Architecture |
| `PRD/appendices/` | Compliance traceability, vendor index, glossary, adversary context. | Audit / procurement |
| `matrix/` | Source CSVs + cross-vendor summary. | Analysts (pivot tables) |

## How to read the interactive report (XYZ-Secrets-Report.html)

Five tabs:
1. **XYZ posture** — where XYZ stands across 47 use cases; tick the PARTIALs
   you consider MET and the posture recomputes.
2. **By use case** — pick a use case → best-fit vendors (by layer) + the
   mapped APRA CPS 234 / ASD ISM controls + XYZ's current state + the
   recommended action.
3. **By identity** — pick a machine-identity type → which vendors cover it.
4. **Compliance trace** — cascade from a regulatory control → the use cases
   it demands → vendor evidence (3 clicks; defaults to APRA CPS 234).
5. **Browse all** — the full capability matrix.

## Read this first (so the numbers aren't misread)

- **18 ranked vendors** across two layers — L1 secrets management (the vault
  tier) and L2 NHI governance (above the vault). A `NATIVE` score means a
  *different thing* in each: L1 = brokers secrets; L2 = discovers/governs.
- **Fortanix DSM is a Layer-0 crypto-substrate dependency**, not a ranked
  vendor — you pair it with a vault, not shortlist it against one.
- **Confidence:** capability existence is vendor-doc-cited; **maturity
  scores (0-4) are analyst judgment, not independently verified**; some GA
  dates are unverified vendor roadmap (see PRD §8.1).

## To share

Email **XYZ-Secrets-Report.html** as an attachment (one file, opens
offline). For a PDF, open it in a browser and use *Print → Save as PDF*.
Keep within XYZ — internal-only pending O2.
