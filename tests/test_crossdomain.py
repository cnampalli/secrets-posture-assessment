import crossdomain


def _row(slug, name, tid, cov, tt="UC-F"):
    return {"vendor_slug": slug, "vendor_name": name, "target_id": tid,
            "target_type": tt, "coverage": cov, "maturity": "3"}


# ownership: conjur + pam roll up to the cyberark parent; others are their own parent
OWN = {"cyberark-conjur": {"parent": "cyberark"}, "cyberark-pam": {"parent": "cyberark"}}


def _domains_data():
    secrets = [_row("cyberark-conjur", "Conjur", "UC-F-001", "NATIVE"),
               _row("cyberark-conjur", "Conjur", "UC-F-002", "NATIVE"),
               _row("hashicorp-vault", "Vault", "UC-F-001", "NATIVE")]
    pam = [_row("cyberark-pam", "CyberArk PAM", "UC-P-001", "NATIVE"),
           _row("beyondtrust", "BeyondTrust", "UC-P-001", "NATIVE")]
    return [{"slug": "secrets", "label": "Secrets", "ranked": secrets},
            {"slug": "pam", "label": "PAM", "ranked": pam}]


def test_parent_rollup_spans_and_native_ucs():
    m = crossdomain.build_crossmap(_domains_data(), OWN)
    assert [d["slug"] for d in m["domains"]] == ["secrets", "pam"]
    cyber = next(p for p in m["parents"] if p["parent"] == "cyberark")
    assert cyber["spans"] == 2
    assert cyber["domains_present"] == ["secrets", "pam"]
    assert cyber["by_domain"]["secrets"]["native_ucs"] == 2   # UC-F-001, UC-F-002
    assert cyber["by_domain"]["pam"]["native_ucs"] == 1
    assert [b["slug"] for b in cyber["by_domain"]["secrets"]["brands"]] == ["cyberark-conjur"]
    bt = next(p for p in m["parents"] if p["parent"] == "beyondtrust")
    assert bt["spans"] == 1
    assert m["parents"][0]["parent"] == "cyberark"
