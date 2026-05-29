import pathlib
import engagement_config as ec

ROOT = pathlib.Path(__file__).resolve().parent.parent
PRESETS = ROOT / "matrix" / "config" / "presets"
AVAILABLE = ["essential-8", "cisa-ztmm-v2", "apra-cps-234", "apra-cps-230",
             "apra-cpg-234", "asd-ism", "mitre-attack"]


def test_default_is_all_frameworks_high_irap():
    cfg = ec.resolve(available=AVAILABLE)
    assert cfg.is_default is True
    assert cfg.residency_weight == "high"
    assert cfg.irap_required is True


def test_preset_financial_scope(tmp_path):
    cfg = ec.resolve(preset="financial", available=AVAILABLE, presets_dir=PRESETS)
    assert set(cfg.framework_scope) == {
        "apra-cps-234", "apra-cps-230", "apra-cpg-234", "essential-8", "cisa-ztmm-v2"}
    assert cfg.is_default is False
    assert cfg.residency_weight == "high"


def test_baseline_always_unioned(tmp_path):
    cfg_path = tmp_path / "e.yaml"
    cfg_path.write_text("primary: [asd-ism]\nresidency: {weight: high, irap_required: true}\n")
    cfg = ec.resolve(config_path=cfg_path, available=AVAILABLE, presets_dir=PRESETS)
    assert "essential-8" in cfg.framework_scope          # baseline default union'd


def test_cli_frameworks_override_preset():
    cfg = ec.resolve(preset="financial", cli_frameworks=["asd-ism"],
                     available=AVAILABLE, presets_dir=PRESETS)
    assert "asd-ism" in cfg.framework_scope
    assert "apra-cps-234" not in cfg.framework_scope     # CLI replaced primary


def test_unknown_slug_warned_and_skipped(tmp_path, capsys):
    cfg_path = tmp_path / "e.yaml"
    cfg_path.write_text("primary: [asd-ism, privacy-act]\n")
    cfg = ec.resolve(config_path=cfg_path, available=AVAILABLE, presets_dir=PRESETS)
    assert "privacy-act" not in cfg.framework_scope
    assert "privacy-act" in capsys.readouterr().err      # warned on stderr


def test_unknown_preset_raises():
    import pytest
    with pytest.raises(ec.ConfigError):
        ec.resolve(preset="nonprofit", available=AVAILABLE, presets_dir=PRESETS)


def test_bad_weight_raises(tmp_path):
    import pytest
    cfg_path = tmp_path / "e.yaml"
    cfg_path.write_text("primary: [asd-ism]\nresidency: {weight: extreme}\n")
    with pytest.raises(ec.ConfigError):
        ec.resolve(config_path=cfg_path, available=AVAILABLE, presets_dir=PRESETS)


def test_weight_off_yaml_boolean_coercion(tmp_path):
    # PyYAML turns bare `off` into False; resolve() must treat it as "off".
    cfg_path = tmp_path / "e.yaml"
    cfg_path.write_text("primary: [asd-ism]\nresidency: {weight: off, irap_required: false}\n")
    cfg = ec.resolve(config_path=cfg_path, available=AVAILABLE, presets_dir=PRESETS)
    assert cfg.residency_weight == "off"
    assert cfg.irap_required is False


def test_config_file_preset_key_is_honored(tmp_path):
    cfg_path = tmp_path / "e.yaml"
    cfg_path.write_text("preset: financial\n")
    cfg = ec.resolve(config_path=cfg_path, available=AVAILABLE, presets_dir=PRESETS)
    assert set(cfg.framework_scope) == {
        "apra-cps-234", "apra-cps-230", "apra-cpg-234", "essential-8", "cisa-ztmm-v2"}
    assert cfg.residency_weight == "high"


def test_cli_preset_overrides_config_file_preset(tmp_path):
    cfg_path = tmp_path / "e.yaml"
    cfg_path.write_text("preset: financial\n")
    cfg = ec.resolve(preset="government", config_path=cfg_path,
                     available=AVAILABLE, presets_dir=PRESETS)
    assert "asd-ism" in cfg.framework_scope and "apra-cps-234" not in cfg.framework_scope


def test_config_inline_keys_override_its_own_preset(tmp_path):
    cfg_path = tmp_path / "e.yaml"
    cfg_path.write_text("preset: financial\nprimary: [asd-ism]\n")
    cfg = ec.resolve(config_path=cfg_path, available=AVAILABLE, presets_dir=PRESETS)
    assert "asd-ism" in cfg.framework_scope and "apra-cps-234" not in cfg.framework_scope
