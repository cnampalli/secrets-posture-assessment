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
