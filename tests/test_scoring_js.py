import shutil, subprocess, pathlib
import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]


@pytest.mark.skipif(shutil.which("node") is None, reason="node not available")
def test_js_engine_conforms_to_vectors():
    r = subprocess.run(["node", str(ROOT / "questionnaire" / "scoring.test.mjs")],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr + r.stdout
    assert "vectors OK" in r.stdout
