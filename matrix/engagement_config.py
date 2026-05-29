"""Engagement config resolution for the regulatory overlay engine.

Resolves framework scope + residency tuning from (in precedence order):
CLI frameworks > inline engagement.yaml > named preset > built-in default.
Sole owner of YAML parsing for engagement/preset files."""
import sys

VALID_WEIGHTS = {"high", "medium", "low", "off"}
DEFAULT_BASELINE = ["essential-8"]      # always-on AU baseline (Privacy Act deferred)


class ConfigError(Exception):
    pass


def _require_yaml():
    try:
        import yaml
        return yaml
    except ImportError:
        raise ConfigError("PyYAML required — pip install -r requirements.txt")


def _load(path):
    yaml = _require_yaml()
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


class EngagementConfig:
    def __init__(self, selected, overlays, baseline, residency_weight,
                 irap_required, is_default):
        self.selected = selected
        self.overlays = overlays
        self.baseline = baseline
        self.residency_weight = residency_weight
        self.irap_required = irap_required
        self.is_default = is_default

    @property
    def framework_scope(self):
        seen, out = set(), []
        for s in list(self.selected) + list(self.overlays) + list(self.baseline):
            if s not in seen:
                seen.add(s)
                out.append(s)
        return out


def _validate_slugs(slugs, available, label):
    out = []
    for s in slugs:
        if s in available:
            out.append(s)
        else:
            print(f"WARN: {label} framework '{s}' not in regulatory-trace.csv "
                  f"— skipped (no control mappings yet).", file=sys.stderr)
    return out


def resolve(preset=None, config_path=None, cli_frameworks=None,
            available=None, presets_dir=None):
    available = list(available or [])

    # No selection of any kind -> default = today's full-scope behaviour.
    if not preset and not config_path and not cli_frameworks:
        return EngagementConfig(
            selected=list(available), overlays=[], baseline=[],
            residency_weight="high", irap_required=True, is_default=True)

    data = {}
    if preset:
        ppath = (presets_dir / f"{preset}.yaml") if presets_dir else None
        if not ppath or not ppath.exists():
            raise ConfigError(f"unknown preset '{preset}'")
        data = _load(ppath)
    if config_path:
        data = {**data, **_load(config_path)}   # inline overrides preset

    selected = list(data.get("primary", []) or [])
    overlays = list(data.get("overlays", []) or [])
    baseline = list(data.get("baseline", DEFAULT_BASELINE) or DEFAULT_BASELINE)

    if cli_frameworks:                          # CLI overrides primary entirely
        selected = list(cli_frameworks)

    res = data.get("residency", {}) or {}
    weight = res.get("weight", "high")
    if weight is False:                 # PyYAML coerces bare 'off' -> False
        weight = "off"
    if not isinstance(weight, str):     # e.g. 'on'/'yes' -> True, or a number
        raise ConfigError(f"residency.weight must be one of {sorted(VALID_WEIGHTS)}, "
                          f"got {weight!r}")
    weight = weight.lower()
    if weight not in VALID_WEIGHTS:
        raise ConfigError(f"residency.weight must be one of {sorted(VALID_WEIGHTS)}, "
                          f"got {weight!r}")
    irap_required = bool(res.get("irap_required", True))

    selected = _validate_slugs(selected, available, "primary")
    overlays = _validate_slugs(overlays, available, "overlay")
    baseline = _validate_slugs(baseline, available, "baseline")

    cfg = EngagementConfig(selected, overlays, baseline, weight,
                           irap_required, is_default=False)
    if not cfg.framework_scope:
        raise ConfigError("resulting framework scope is empty after validation")
    return cfg
