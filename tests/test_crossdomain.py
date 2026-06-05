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


def test_parents_carry_display_names():
    m = crossdomain.build_crossmap(_domains_data(), OWN)
    disp = {p["parent"]: p["display"] for p in m["parents"]}
    assert disp["cyberark"] == "CyberArk"           # corporate parent (no brand slug == parent)
    assert disp["beyondtrust"] == "BeyondTrust"     # self-parent → its own brand name
    assert disp["hashicorp-vault"] == "Vault"       # self-parent → brand name from the data
    # the panel entries carry the display name too (so the report never shows a raw slug)
    assert m["concentration"][0]["display"] == "CyberArk"
    assert m["consolidation"][0]["display"] == "CyberArk"


def test_concentration_only_lists_spanning_parents():
    m = crossdomain.build_crossmap(_domains_data(), OWN)
    conc = m["concentration"]
    assert [c["parent"] for c in conc] == ["cyberark"]      # only spans>=2
    c = conc[0]
    assert c["spans"] == 2 and c["brands_total"] == 2       # Conjur + CyberArk PAM
    assert "CPS 230" in c["note"]


def test_consolidation_ranks_spanning_parents_by_breadth():
    m = crossdomain.build_crossmap(_domains_data(), OWN)
    cons = m["consolidation"]
    assert [c["parent"] for c in cons] == ["cyberark"]
    assert cons[0]["domains"] == 2
    assert cons[0]["native_ucs_total"] == 3                 # 2 (secrets) + 1 (pam)


def test_single_domain_only_yields_empty_panels():
    one = [{"slug": "secrets", "label": "Secrets",
            "ranked": [_row("hashicorp-vault", "Vault", "UC-F-001", "NATIVE")]}]
    m = crossdomain.build_crossmap(one, {})
    assert m["concentration"] == [] and m["consolidation"] == []


def test_empty_domain_does_not_error():
    data = [{"slug": "secrets", "label": "Secrets", "ranked": []},
            {"slug": "pam", "label": "PAM", "ranked": []}]
    m = crossdomain.build_crossmap(data, {})
    assert m["parents"] == [] and m["concentration"] == [] and m["consolidation"] == []
