#!/usr/bin/env bash
# Assemble a single emailable package for the XYZ stakeholder review.
# Output: dist/XYZ-Secrets-Management-PRD-v0.1.zip
# INTERNAL — contains [INTERNAL] XYZ findings; keep within XYZ (open question O2).
set -euo pipefail
cd "$(dirname "$0")"

NAME="XYZ-Secrets-Management-PRD-v0.1"
OUT="dist"
STAGE="$OUT/$NAME"

rm -rf "$STAGE" "$OUT/$NAME.zip"
mkdir -p "$STAGE/matrix"

# Regenerate the interactive report fresh from the CSVs.
python3 matrix/build_matrix_viewer.py >/dev/null

# Primary artifact: the self-contained report, friendly name.
cp matrix/matrix-viewer.html "$STAGE/XYZ-Secrets-Report.html"

# Cover note + written package.
cp STAKEHOLDER-START-HERE.md "$STAGE/START-HERE.md"
cp README.md CHANGELOG.md "$STAGE/"
cp -R PRD "$STAGE/PRD"

# Supporting matrices for analysts (markdown summary + source CSVs).
cp matrix/matrix.md "$STAGE/matrix/"
cp matrix/*.csv "$STAGE/matrix/"

# Zip it.
( cd "$OUT" && zip -rq "$NAME.zip" "$NAME" )
SIZE=$(du -h "$OUT/$NAME.zip" | cut -f1)
echo "Package ready: $OUT/$NAME.zip ($SIZE)"
echo "Primary artifact inside: $NAME/XYZ-Secrets-Report.html (email this single file for a quick view)"
