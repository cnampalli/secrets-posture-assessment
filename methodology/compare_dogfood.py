"""Compare the rubric dogfood re-score against the frozen baseline verdicts."""
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]


def _load(path, key, val):
    with open(path, newline="", encoding="utf-8") as fh:
        return {r[key]: r[val] for r in csv.DictReader(fh)}


def main():
    proposed = _load(ROOT / "methodology" / "posture-rescore.csv", "uc_id", "proposed_state")
    baseline = _load(ROOT / "matrix" / "domains" / "secrets" / "current-state.csv", "uc_id", "current_state")
    matches, diffs = 0, []
    for uc, base in baseline.items():
        prop = proposed.get(uc, "MISSING")
        if prop == base:
            matches += 1
        else:
            diffs.append((uc, base, prop))
    total = len(baseline)
    print(f"Reproduction: {matches}/{total} = {matches/total:.0%}")
    print("Divergences (uc_id: baseline -> proposed):")
    for uc, base, prop in sorted(diffs):
        print(f"  {uc}: {base} -> {prop}")


if __name__ == "__main__":
    main()
