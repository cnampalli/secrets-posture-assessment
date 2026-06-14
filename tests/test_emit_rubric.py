import json, pathlib
import questionnaire.emit_rubric as emit

ROOT = pathlib.Path(__file__).resolve().parents[1]


def test_emits_both_domains(tmp_path, monkeypatch):
    # redirect output into a temp app/src/data so the test never clobbers the repo copy
    out_dir = tmp_path / "data"
    monkeypatch.setattr(emit, "OUT_DIR", str(out_dir))
    emit.main()
    secrets = json.loads((out_dir / "rubric.secrets.json").read_text(encoding="utf-8"))
    pam = json.loads((out_dir / "rubric.pam.json").read_text(encoding="utf-8"))
    iga = json.loads((out_dir / "rubric.iga.json").read_text(encoding="utf-8"))
    assert len(secrets) == 50      # M3.2: +3 agent-credential UCs (UC-F-028/029/030)
    assert len(pam) == 18
    assert len(iga) == 19          # M3.1: +3 agentic governance UCs (UC-I-017/018/019)
    assert {u["uc_id"] for u in pam} == {f"UC-P-{i:03d}" for i in range(1, 19)}
    assert {u["uc_id"] for u in iga} == {f"UC-I-{i:03d}" for i in range(1, 20)}
    assert all("uc_id" in u and "questions" in u or u["kind"] == "bespoke" for u in secrets)


def test_domains_registry_drives_output():
    ids = {d["id"] for d in emit.DOMAINS}
    assert {"secrets", "pam", "iga"} <= ids
