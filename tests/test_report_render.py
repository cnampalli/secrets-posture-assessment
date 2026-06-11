import hashlib, pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
ENGINE = ROOT / "matrix" / "build_matrix_viewer.py"
SNAPSHOT = ROOT / "tests" / "fixtures" / "report.snapshot.html"


def test_default_report_is_byte_identical(tmp_path):
    # Build the default report and compare to the frozen snapshot, byte-for-byte.
    subprocess.run([sys.executable, str(ENGINE)], cwd=ROOT, check=True,
                   capture_output=True)
    built = (ROOT / "matrix" / "domains" / "secrets" / "secrets-report.html").read_bytes()
    frozen = SNAPSHOT.read_bytes()
    assert hashlib.md5(built).hexdigest() == hashlib.md5(frozen).hexdigest(), \
        "report HTML changed vs frozen snapshot"
