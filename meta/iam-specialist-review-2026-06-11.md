# Independent IAM Specialist Review — Posture-Assessment Instrument

**Date:** 2026-06-11
**Reviewer:** Senior IAM specialist (15+ yrs workforce IAM / PAM / IGA / machine identity; bank-advisory background). No prior exposure to this repository; all in-repo documents treated as author claims and market assertions verified by live research where they matter.
**Scope reviewed:** methodology (`methodology/`), all three domain datasets (`matrix/domains/{secrets,pam,iga}/`), built HTML reports, React + static questionnaires, PRD + ADRs, research corpus (`research/`), vendor-intel config (`matrix/config/`), presentation layer. Tests run read-only: **308 pytest pass, `validate_data.py` clean** (verified 2026-06-11).

---

## (a) One-page overall verdict

**This is a genuinely credible, above-market practitioner instrument with one strategic weakness (no benchmark/calibration) and two data-currency defects in exactly the feature it sells hardest.** I would put it in the top decile of maturity-assessment tooling I have seen from boutique consultancies, and ahead of the vendor-funnel assessments (SailPoint Horizons, CyberArk ISMM, Delinea maturity model) on methodological honesty. It is not yet ahead of them on the things buyers notice first: benchmarks, brand authority, and a 15-minute entry tier.

**What is genuinely good** (and rarer than the author may realise):
- The **archetype rubric** (A0–A8, parametrised MET/PARTIAL/GAP definitions, six scoring dimensions, deterministic derivation + mandatory override rationale, independent confidence axis, PENDING as a first-class state) is a real instrument design, not a survey. Most market "maturity assessments" are self-attested Likert surveys; this one demands evidence artifacts per verdict (`evidence-catalog.csv` with tiers, named artifacts, sensitivity tags, control citations).
- The **NHI taxonomy (37 types)** crossed with 47 use cases and a layered (L0/L1/L2) vendor stack is a more complete machine-identity content map than anything publicly offered by Gartner, KuppingerCole, or the NHI vendors themselves.
- **Honesty engineering** — anti-fabrication validators, `framework_role` honesty (BACK-MAP vs INFORMATIVE), "UNVERIFIED against primary" survives into the rendered report, maturity scores labelled analyst judgment. Regulators and bank 2LoD functions notice this; it is the difference between an instrument that survives challenge and one that doesn't.
- The **AU regulatory spine** (APRA CPS 234/230, ASD ISM, Essential 8, back-mapped per UC with a 3-click compliance-trace view) is a real wedge: the Big-4 build this bespoke per engagement; nobody productises it.

**What undermines it today:**
1. **Vendor-ownership data is wrong in two places that matter** — `matrix/config/vendor-ownership.yaml` asserts Entro Security is a CyberArk subsidiary (no such acquisition exists; Entro is an independent Series-A company), and it **misses Palo Alto Networks' completed $25B acquisition of CyberArk (closed 2026-02-11)** — the largest deal in security-industry history and the single most important concentration fact for any cross-domain consolidation view. The cross-domain report's headline ("CyberArk spans 2/2 domains") is materially understated: the true parent now spans PAM + secrets + machine-identity PKI (Venafi) + IGA-adjacent (Zilla) + the network/SOC estate. For a product whose flagship cross-domain feature is *parent-aware concentration analysis*, this is a fabrication-class defect — in a project with a documented fabrication history and guards built specifically to prevent this.
2. **No external calibration, no peer benchmark, no maturity roll-up.** Every serious competitor (SailPoint Horizons: annual survey of hundreds of orgs; KuppingerCole: benchmark against its Reference Architecture; CyberArk ISMM: ESG survey of 1,500 professionals) leads with "here's where you sit vs peers." This instrument cannot answer a CISO's first question.
3. **Scoring discrimination is coarse.** Quantitative questions ("What share of the population has migrated?") are answered yes/no/na (`app/src/assessment/scoring.ts`), and a single GAP-gate "no" forces GAP. Right for defensibility, wrong for showing progress between assessments — a bank that moves 20%→80% migrated still scores the same.

**Verdict: invest.** The asset is real, the market timing is right (NHI ~40% category growth; agentic-AI identity is the 2026 theme every acquirer is paying for), and the defects are weeks of work, not a redesign. Fix the ownership data, build the roll-up + rapid-scan tier, and start accumulating benchmark data from the first three engagements.

---

## (b) The ten questions

### 1. What do I think of the tool overall?

**Strong instrument core, mid-maturity product surface, weak go-to-market.** The four-layer build (CSV data → domain descriptor → archetype engine → self-contained offline HTML report) is well-engineered and verified green (308 tests, byte-stable rebuilds). The methodology documents (`methodology/METHODOLOGY.md`, `RUBRIC.md`, `PLAYBOOK.md`, `FACILITATOR-GUIDE.md`) form a complete delivery system — a non-technical facilitator genuinely could run this, which is the hardest part of productising consulting IP.

Three design choices I want to single out as *correct against industry practice*:
- **Capability-presence over flat ranking** (`iga-vendor-fit.csv` is NATIVE/PARTIAL/ADD-ON per functional area; the secrets stack is layered L0/L1/L2 with "paired, not ranked" for the crypto substrate). Flat cross-category vendor rankings are how consultancies get sued and how buyers get misled.
- **PENDING as a state, not a low score.** Most instruments force a guess; this one surfaces missing signal as an open item. That is exactly how a regulator wants to see it.
- **Override protocol** (proposed_state vs final_state + mandatory rationale). This is the documented-judgment pattern audit firms use; almost no security maturity tool implements it.

Honest weaknesses beyond the three in the verdict: the secrets domain (47 UCs, ~140 questions) is heavyweight for a first engagement; the report's "Business value" framing is appropriately illustrative but the exec narrative still depends on a single anonymised reference customer; and the instrument has been applied end-to-end exactly once (the XYZ/Task-0 pass), so facilitator-independence is unproven.

### 2. Per-stakeholder value (CEO, CISO, CIO, CTO, Product Owners, Product Area Leads, IAM engineers)

See the matrix in §(c). Summary judgment: **the CISO and the IAM Product Owner are the real users; the CEO and CIO are read-only consumers of derivatives; engineers will use the data files more than the reports.** The biggest per-stakeholder misses: no peer benchmark (CEO/CISO), no cost/TCO dimension (CIO), no exportable backlog format (Product Owners), and no remediation how-to patterns (engineers).

### 3. Is the NHI taxonomy inside the secrets assessment a valid addition worth investing in?

**Yes — it is the most valuable single asset in the repo.** Evidence: `research/identity-taxonomy.md` (37 NHI types, five classification axes — lifecycle, trust anchor, auth shape, governance maturity, human-shared — anchored to CSA NHI WG, SPIFFE, Sigstore, NIST SP 800-63-4/800-204D), carried into `matrix/domains/secrets/identity-catalog.csv` and crossed with every use case and vendor cell.

Why it's right, against the market: secrets management *without* an identity taxonomy is just vault hygiene. The industry has converged on exactly this framing — CSA's NHI working group, OWASP's Non-Human Identities Top 10 (2025), Gartner's machine-identity push, and the entire NHI vendor category (Astrix, Oasis, Entro, Aembit, Clutch — all profiled in `research/vendors/`) sell "you can't govern what you can't enumerate." The taxonomy is what turns the assessment's headline finding ("no NHI inventory layer above the vault") from an opinion into a measurable population statement. The long tail (NHI-015 code-signing, NHI-018 TEE attestation, NHI-027 on-behalf-of holders, NHI-037 orphaned identities) is more complete than any vendor-published taxonomy I can find.

Investment caveats: (i) keep it current quarterly — agentic subtypes are fragmenting fast (MCP servers/tools, agent-framework identities, A2A delegation chains deserve NHI-019 sub-rows); (ii) publish an explicit mapping to the CSA taxonomy and OWASP NHI Top 10 for external credibility; (iii) the COMMON/UNCOMMON tags are author judgment — fine, but say so in the legend.

### 4. Is the owner following an IAM → NHI → Agentic-AI pathway? Where is it real vs aspirational?

**The pathway is real through the first two stages and aspirational at the third.**
- **IAM (real):** PAM (18 UCs, 10 vendors) and IGA (16 UCs, 8-vendor fit grid) are stood up as full domains on the shared engine; the roadmap (`docs/superpowers/MULTI-DOMAIN-ROADMAP.md`) explicitly sequences secrets → PAM → IGA → workforce IAM (demand-pulled). That is a coherent identity-domain progression, not a secrets tool with bolt-ons.
- **NHI (real):** the secrets domain *is* an NHI-governance instrument (see Q3); PAM carries 8 non-human privileged classes (A2A, CI/CD, governed service accounts) and IGA carries governed-service-account + consent-grant classes with continuous-attestation framing.
- **Agentic AI (aspirational):** what exists is taxonomy rows (NHI-019, NHI-020; IGA's IGID-012 agentic-AI), two secrets UCs (UC-F-018 LLM tool-credential brokering, UC-N-019 AI-agent KPI suite — both well-written, citing OWASP LLM Top 10 and CSA), and one IGA evidence item (EV-IGA-AGENTIC-OAUTH-ATTESTATION). What does *not* exist: an agentic identity assessment domain or even a UC cluster covering delegation-chain provenance, human-in-the-loop authorization gates, agent-to-agent auth (MCP/A2A), agent session containment, or model-supply-chain identity. PAM — the domain where agentic privilege is most acute — has **zero** agent content (its own review flags this, B8 = Emerging).

The market has already moved to stage three: Delinea bought StrongDM explicitly "to secure AI agents with continuous identity authorization" (closed 2026-03-05); Palo Alto framed the CyberArk close as "secure the AI era"; Microsoft, Okta and Ping all shipped agent-identity offerings; CSA published "Agentic AI Identity and Access Management: A New Approach." The owner's direction is right and earlier than most consultancies — but today the agentic layer is ~5% of the artifact mass. Calling the pathway "in place" would be overclaiming; calling it "the designed next step with the rails already laid" is accurate, because the archetype engine genuinely would absorb an agentic domain without modification (the IGA hybrid proved the engine handles process-shaped domains).

### 5. Are the PAM and IGA assessments legitimate practitioner instruments? Improvements?

**Yes, both clear the legitimacy bar.**
- **PAM (18 UCs):** the catalog spans the full canonical set — vaulting/rotation, session isolation + recording, JIT/ZSP, discovery, A2A brokering, MFA-for-priv, break-glass, EPM, entitlement right-sizing, vendor remote access, CIEM, secretless attestation, certification, threat analytics, credential-theft detection, resilience, SAW/PAW (`matrix/domains/pam/use-cases.csv`). The identity catalog (20 PID classes, incl. tier-0 directory, hypervisor admin, SaaS super-admin, vault-operator "keys to kingdom") is the population a bank actually has. The evidence catalog is the standout: each item names a concrete artifact ("vault onboarded-accounts export," "rotation-failure alert rule and a sample ticket") with tier and sensitivity. That is audit-grade and better than most Big-4 workpaper templates I've seen.
- **IGA (16 UCs):** JML, certification (periodic + event-driven + high-risk sign-off), SoD (preventive + detective + register), role mining, request workflow, self-approval prevention, unstructured-data entitlements. Right-sized (IGA assessments die of scope bloat), and the identity catalog is unusually thoughtful — IGID-005 "privileged business user (not infrastructure admin, which is PAM's domain)" shows real domain-boundary discipline; IGID-008 SoD-sensitive finance roles is the SOX/ICFR class consultants always probe. The vendor-fit grid honestly grades Entra/Okta SoD as PARTIAL and preserves "marketing-grade" caveats per cell — correct, and unusual.

**Improvements (priority order):**
1. **PAM: add agentic/AI privileged access** — agent-initiated privileged sessions, JIT for agent identities, human-approval gates on high-risk agent actions. This is the 2026 buying conversation (see Delinea/StrongDM rationale).
2. **Both: maturity roll-up** (e.g. ML1–ML3 per capability area) — the data supports it; boards can't consume 18–47 row verdicts.
3. **IGA: add UCs for agent lifecycle governance and SaaS-to-SaaS OAuth-grant certification** (the taxonomy rows exist; the UCs don't), plus machine-identity certification as a first-class campaign type (the PAM/IGA seam where service accounts fall today).
4. **PAM: ITDR linkage** — UC-P-015/016 gesture at detection, but the ITDR product category (CrowdStrike, Microsoft, Silverfort) deserves explicit adjacency treatment like CIEM got.
5. **Both: calibration workbook** — 3–5 worked scoring examples per domain so a second facilitator scores the same evidence the same way. Inter-rater reliability is currently a design intent, not a demonstrated property.
6. **Britive evidence re-anchor** before any client use (the repo itself flags it marketing-tier — do it, don't ship the caveat).

### 6. What differentiates this methodology vs the market — honestly?

I checked the instrument against the live market. The comparison set:
- **Gartner IAM Program Maturity Model / IT Score** ([gartner.com](https://www.gartner.com/en/documents/3993765)): program-level (governance, org structure, vision, process), five CMM levels, self-assessed, paywalled. Not control-level, not evidence-demanding, no vendor layer.
- **KuppingerCole IAM Maturity Assessment** ([kuppingercole.com](https://www.kuppingercole.com/advisory/iam-maturity-assessment)): 50 questions across 17 capabilities, 10–15 minutes, benchmarked against their Reference Architecture. Broad IAM, shallow per control, no evidence artifacts.
- **SailPoint Horizons** ([sailpoint.com](https://www.sailpoint.com/horizons/assessment)): 6-question instant self-check + a genuinely good annual research benchmark; funnels to SailPoint. Now explicitly covers "humans, machines, and AI agents."
- **CyberArk Identity Security Maturity Model / Blueprint** ([cyberark.com](https://www.cyberark.com/identity-security-maturity-model/)): ESG survey-derived four-tenant model + the Blueprint roadmap method; vendor-funnel, but the breadth-vs-depth lens is good.
- **Delinea Identity Security Maturity Model** ([delinea.com](https://delinea.com/solutions/identity-security-maturity-model)): PAM-centric staged model; vendor-funnel.
- **KPMG IAM Maturity Assessment** ([kpmg.com](https://kpmg.com/hu/en/services/advisory/technology/cybersecurity/identity-and-access-management-services/iam-maturity-assessment.html)) and Big-4 peers: CMMI/COBIT-aligned, vendor-independent, bespoke per engagement, expensive, methodology not published.
- **CSA / OWASP**: NHI taxonomy, "State of NHI and AI Security" survey, Agentic AI IAM guidance ([cloudsecurityalliance.org](https://cloudsecurityalliance.org/artifacts/agentic-ai-identity-and-access-management-a-new-approach)) — frameworks and surveys, not assessment instruments.

**Genuine differentiators (defensible):**
1. **Evidence-demanding, falsifiable verdicts.** Nobody in the list above binds every verdict to a named evidence artifact with tier + sensitivity + control citation, plus an assessor-override audit trail. This is the instrument's moat with risk functions and APRA-regulated buyers.
2. **NHI-first depth.** A 37-type NHI taxonomy × use-case × vendor-capability matrix does not exist as a product anywhere — the NHI vendors have discovery tools, the analysts have market guides; nobody has the assessment instrument.
3. **Productised AU regulatory trace.** Per-UC APRA CPS 234 / ASD ISM / E8 back-mapping with a 3-click control→UC→evidence cascade. Big-4 do this bespoke at bespoke prices; no productised competitor in the AU market.
4. **Vendor neutrality at a moment of extreme consolidation.** Post PANW-CyberArk, post Delinea-StrongDM, post IBM-HashiCorp, the number of credible *neutral* assessors is shrinking. A layered, no-flat-ranking, confidence-labelled vendor view is worth more in 2026 than it was in 2024 — provided the ownership data is right (see defect above; today it isn't).
5. **Cross-domain on one engine** — same rubric semantics across secrets/PAM/IGA so posture is comparable across domains. Vendor models can't do this neutrally; analyst models don't go this deep.

**Not differentiated (don't pretend otherwise):**
- Maturity levels / staged models — everyone has one (and this instrument actually *lacks* the roll-up everyone else leads with).
- Benchmarking — SailPoint, CyberArk/ESG, KuppingerCole all have peer data; this has none. Today that's a deficit, not a parity.
- Brand authority and distribution — Gartner/KC/Big-4 logos close deals; this needs a lighthouse client and a published methodology paper to compete.
- Speed-to-first-insight — KC is 15 minutes, SailPoint is 6 questions; this is an 8–12-week facilitated engagement with no triage tier.

### 7. Is the questionnaire accurate?

**Substantially yes — the question set genuinely evidences the maturity states it claims — with three structural caveats.**

What I verified: the archetype question templates (`methodology/archetype-questions.csv`) map 1:1 onto the dimensions that the state definitions (`assessment-archetypes.csv`) declare load-bearing; the parametrisation pipeline (`uc-archetype-map.csv` → `emit_rubric.py` → `rubric.{secrets,pam,iga}.json`) instantiates them concretely and correctly (e.g. UC-F-003 renders "Is OIDC federation (sub/aud-scoped) the enforced default for new cloud IAM pipeline credentials?" — exactly the A2 enforcement gate). Counts: secrets 47 UCs/140 questions, PAM 18/58, IGA 16/51, all consistent across the static questionnaires and the React app, all validated by the test suite. The questions probe the right discriminators — blocking-vs-detect mode, shelf-ware vs adopted, burn-down inventories, owner+expiry exceptions, alert-on-failure — which is precisely what separates real maturity from deployed-capability theatre. Bespoke criteria (A0) for the genuinely unique UCs (TEE attestation, vault-internal hardening) are technically correct and current.

Caveats:
1. **Answer-type mismatch:** quantitative questions ("What share of existing {population} has migrated…?", A2-Q2; A3-Q2; A5-Q2) are captured as yes/no/na (`scoring.ts` VALID = yes|no|na). The facilitator must mentally apply the threshold; the recorded answer loses the number. Capture the percentage and let the rubric apply the threshold — you'll also get trend data for free.
2. **Hard gating compresses signal:** any GAP-informing "no" → GAP regardless of other answers; partial credit and weighting don't exist. Defensible, but it can't show movement between re-assessments (the methodology's own re-assess stage needs that).
3. **One enforcement gap the author also knows about:** confidence and evidence capture are not *enforced* at answer time — a facilitator can record yes/no without naming the artifact, silently degrading the instrument's core differentiator. Make evidence-ref a required field for any MET-contributing answer.

Accuracy of content itself: I spot-checked thresholds and control IDs against my own knowledge and the repo's verification trail (ISM corrections documented in `matrix/ISM-CONTROL-VERIFICATION-2026-05-24.md`; two more fabrication-class ISM IDs caught and fixed in WS1). The remaining data-hygiene flags the repo carries honestly (dangling citation keys, one off-by-one REG count) are minor. The questionnaire is accurate enough to defend in front of a bank 2LoD function today.

### 8. Should NHI + Agentic-AI identities AND privileged identities be included across PAM, secrets, AND IGA? Coverage model?

**Yes — and the right model is one shared identity spine with per-domain lenses, not per-domain catalogs that drift.**

Current state is asymmetric: secrets has 37 NHI types incl. AI agents but pushes privileged human operators out of scope (NHI-024/025 marked "out of NHI scope"); PAM has 20 classes incl. 8 non-human but **no agentic-AI class**; IGA has agentic-AI + consent-grants but only 3 NPE classes. Each catalog was authored per-domain (`identity-catalog.csv` ×3) with no cross-references — the same real-world object (a privileged service account) appears as NHI-012, PID-005, and IGID-009 with no linkage.

Why full tri-domain coverage is right, as a practitioner: the *identity* doesn't care about your product taxonomy. An AI agent holds secrets (secrets domain), takes privileged actions (PAM domain), and needs ownership/attestation/lifecycle (IGA domain). A bank's auditor will ask "show me the posture of your AI agents" — the answer today requires opening three reports and reconciling by hand. The market agrees: every 2026 platform move (PANW/CyberArk, Delinea/StrongDM, SailPoint's machine-identity + agent governance push, Entra Agent ID) is the *vendors* unifying these planes; an assessment instrument that keeps them siloed will read as last-generation within 18 months.

**Recommended coverage model:**
1. **Single cross-domain identity registry** (one CSV/YAML, like `vendor-ownership.yaml` already does for vendors): each identity class keyed once, tagged with `human | npe | agentic` and `privileged: y/n`, with per-domain applicability flags.
2. **Per-domain lenses, not per-domain truths:** secrets assesses the *credential lifecycle* of each class; PAM assesses *session/elevation control*; IGA assesses *ownership, attestation, lifecycle governance*. Same identity, three orthogonal question sets — the archetype engine already supports this (the dimensions differ; the population doesn't).
3. **A cross-domain "identity-class coverage" view** in `cross-domain-report.html`: rows = identity classes, columns = domains, cells = posture. That view is the agentic-AI story the market is buying and would be a genuine first.
4. **Minimum immediate additions:** agentic-AI privileged class in PAM; agent lifecycle + OAuth-grant UCs in IGA; keep privileged human operators in secrets as cross-references (don't re-assess them, point to PAM).

### 9. Do the use cases read like real business requirements? Where's the gap to a real bank's requirement set?

**They read like a very good analyst's requirement-shaped catalog, validated against exactly one real bank — which is visible in the texture.**

Where they read like real requirements: every secrets UC has a persona story, testable acceptance criteria, in-scope identity population, control back-map, and priority (`research/use-cases.md`) — that is requirement form, and better-formed than most bank backlog items I've seen. Crucially, the *current-state* layer is grounded in genuine lived evidence from a live stakeholder session (a 2019 red-team plaintext-secrets finding still open; Vault JIT covering AWS only, not Azure/GCP; no NHI inventory above the vault — `research/anz-current-state-evidence.md`, `current-state.csv`). Those are real-bank fingerprints, and they anchor UC-F-001/002/003 in a way no analyst construct can fake. The seed UCs that came from the user (UC-F-001, UC-N-001) are indistinguishable from a bank's actual problem statements because they are.

Where they read like analyst constructs: the thresholds (95% migration, 12-month deprecation, 15-minute alert SLA) are sensible defaults, not negotiated numbers; the long tail (UC-F-017 TEE attestation, UC-F-024 FAPI 2.0, UC-N-013 PQC readiness) is completeness-driven breadth a bank's product owner would never have written unprompted; and PAM/IGA UCs are derived from canonical practice (Gartner MQ scope, ISM controls) rather than extracted from any requirement register — competent, but no lived fingerprints yet.

**Gap to a real bank's requirement set** (what's missing if you handed this to a bank's design authority as "the requirements"):
- **Platform NFRs:** availability/RTO/RPO for the secrets/PAM service itself, latency budgets, DR and break-glass *of the vault*, capacity volumetrics (secrets/sec, session concurrency).
- **Integration constraints:** ServiceNow/CMDB, SIEM destinations, HR feed specifics, existing EA standards and approved-pattern catalogs.
- **Operating model:** who runs it (platform team vs CyberArk managed), support tiers, chargeback. Banks fight harder over this than over capability.
- **Commercials:** licensing model constraints, panel-vendor requirements, exit/portability clauses (APRA CPS 230 material-service-provider obligations).
- **Risk-appetite parametrisation:** the thresholds should be per-client knobs tied to the bank's own risk appetite statements (the `params` mechanism supports this — use it in engagement config rather than shipping defaults as truth).
- **Migration sequencing constraints:** freeze windows, change-control cadence, regulatory-program collision (the things that actually determine a bank's roadmap order).

None of this is fatal — an assessment instrument is not a solution design — but the PRD framing ("the product is a report") sometimes blurs that line; keep the claim at "requirements-shaped findings catalog," not "your requirement set."

### 10. What else would I add as a trusted advisor?

**Data-currency risk is your existential risk.** The instrument's credibility rests on citations being true. I found two ownership errors in one config file in one afternoon (Entro≠CyberArk; missing PANW-CyberArk close). Vendor capabilities, GA dates, and ownership now decay on a ~monthly cycle because of M&A velocity ($96B of identity M&A in 2025 per market reporting). You need a **dated re-verification cadence per source tier** (the `data-provenance.yaml` scaffolding exists — operationalise it) and a pre-engagement "currency gate" that fails the build if any HIGH-impact fact is older than N days.

**Anonymisation leakage.** The shipped HTML is clean (I checked — the "ANZ" hits in it are font base64), but the repo itself still carries the real client name in filenames and content (`research/anz-current-state-evidence.md`, `task0/responses.md`), and the README's recommended sharing mode is "zip the whole research-papers/ directory." That combination *will* leak the reference client's identity the first time someone follows the README. Separate the client-evidence layer from the product repo before any external distribution.

**Market timing — favourable, window is 12–24 months.** NHI is the fastest-growing identity category (~40%/yr; multiple analysts), agentic-AI identity is the universal 2026 theme, and consolidation is destroying vendor-neutral advice supply. But the platforms (PANW, SailPoint, Delinea, Microsoft) are all shipping free maturity assessments as funnels, and the analysts will productise NHI maturity within a year or two. Move now; the differentiation decays.

**Packaging/pricing:** sell three tiers — (1) **Rapid scan** (the missing triage tier: ~25 questions, 2 workshops, fixed low fee) as the wedge; (2) **Full domain assessment** (current 8–12-week instrument) at boutique fixed fee; (3) **Posture retainer** (quarterly re-assess + board pack + benchmark membership). The benchmark only exists if tier-3 clients contribute anonymised data — design the consent and anonymisation now, because the benchmark becomes the moat. Consider publishing the archetype model + taxonomy as an open methodology paper (the KC/CSA play): you give away the schema, you sell the facilitation, calibration, and data.

**Regulatory angles to exploit:** APRA CPS 230 (in force since July 2025) makes service-account and third-party dependency mapping board-level — your evidence model is naturally adjacent; build the CPS 230 overlay. CPS 234 tripartite reviews need exactly the evidence packs this generates. For expansion: EU DORA and NIS2 overlays are the same back-map exercise with different control IDs — the `frameworks.yaml` engine claims to support exactly this; one EU overlay would prove portability and double the addressable market.

**Risks the owner should hold:** single-author calibration (every verdict so far reflects one person's judgment — get a second assessor to blind-score one engagement and publish the agreement rate); IP leakage (the CSVs are the product; a shared zip is the product given away — consider rendering-only distribution); and over-engineering pull (the engine is already ahead of the product surface — the next dollar belongs in benchmark data and a second reference client, not more engine).

---

## (c) Stakeholder-value matrix

| Stakeholder | Value today | Gap | Would they use it? |
|---|---|---|---|
| **CEO** | `value-proposition.html` + exec summary give a 2-page cost-avoidance narrative; honest "illustrative" posture avoids invented-ROI embarrassment. | No peer benchmark ("are we behind?"), no single maturity number trending over time, no dollar quantification tied to *their* loss data. | **No — reads a derivative once.** Would glance at a one-page board tile; needs the roll-up + benchmark to care. |
| **CISO** | The real buyer. Defensible gap report, 3-click regulator trace (CPS 234/ISM/E8), evidence-backed verdicts that survive 2LoD challenge, prioritised risk×effort roadmap, vendor-neutral consolidation view. | Maturity roll-up for board comms; peer benchmark; rapid-scan tier for first contact; ITDR/threat-detection linkage thin. | **Yes — primary user.** Would commission it and defend it internally; would push the report at audit time. |
| **CIO** | Cross-domain vendor concentration view (consolidation $ angle); rationalisation evidence for overlapping tooling; APRA posture story. | No TCO/licensing dimension; ownership data currently wrong (PANW-CyberArk missing) which is precisely the CIO's question; no integration-effort sizing. | **Partially — consumes the vendor chapters.** Would use the cross-domain view in strategy papers once ownership data is fixed. |
| **CTO** | Architecture-current content (SPIFFE, secretless, OIDC federation, TEE, layered stack model); taxonomy as a shared engineering vocabulary; honest "compose, don't displace" guidance. | No reference architectures or target-state blueprints; platform NFRs absent; agentic patterns thin. | **Yes, selectively.** Would cite the taxonomy and layer model in design authority; wouldn't run the instrument. |
| **Product Owners (IAM tooling)** | 47/18/16 requirement-shaped UCs with acceptance criteria = ready-made backlog seed; per-UC vendor capability evidence for build-vs-buy. | No export to backlog formats (Jira/ADO CSV); no story sizing; thresholds not parametrised to their org; no API. | **Yes — would mine it.** Would copy-paste UCs into backlog; an exporter would make this a daily tool. |
| **Product Area Leads** | Engagement menu / sequenced roadmap with dependency awareness; PENDING list = funded discovery work; per-area posture for QBRs. | Effort bands are qualitative; no capacity/cost model; no per-area trend view until re-assessment lands. | **Yes, quarterly.** Would use the roadmap to argue priority; needs the re-assess delta view to keep using it. |
| **IAM Engineers** | Evidence catalog tells them exactly what artifact proves what; questionnaire questions are technically literate (blocking-mode, sub/aud scoping, burn-down); vendor CSVs are pivot-table-ready; offline single-file report respects their environment. | No remediation how-to / pattern library behind each GAP; quantitative answers flattened to yes/no; no machine-readable findings export (JSON exists in app but not first-class). | **Yes — the data files more than the report.** Would use the evidence catalog before an audit and the vendor CSVs during selection. |

---

## (d) If this were my product — the next five moves, in order

1. **Fix the vendor-ownership layer this week and add a currency gate.** Correct `vendor-ownership.yaml`: remove Entro→CyberArk (unsupported; Entro is independent), add `cyberark: parent: palo-alto-networks (as_of 2026-02-11)` so PANW concentration (CyberArk PAM + Conjur + Venafi + Zilla) renders truthfully in the cross-domain view; note IBM-HashiCorp is captured — re-verify the rest. Then extend `validate_data.py` with a max-age check per provenance tier. Nothing else matters if the flagship neutral-advice feature states false facts.
2. **Ship the maturity roll-up + rapid-scan tier.** A 3-level per-capability-area roll-up (the data already supports it) for board packs, and a ~25-question triage instrument auto-derived from the GAP-gate questions as the commercial wedge. These two close the most-cited buyer gaps (discrimination, proportionality) in one stroke.
3. **Stand up the agentic-AI slice across all three domains.** PAM: agentic privileged-access class + 2 UCs (agent JIT elevation, human-approval gates). IGA: agent lifecycle + OAuth-grant certification UCs (taxonomy rows already exist). Secrets: sub-type NHI-019 (MCP/tool servers, framework identities). Add the cross-domain identity-class coverage view. This converts the IAM→NHI→Agentic pathway from aspiration to artifact while it's still early.
4. **Run one paid (or heavily discounted) second engagement with a different facilitator, and instrument it.** Capture inter-rater agreement, time-per-UC, and the client's anonymised posture as benchmark row #1. Fix the capture-layer gaps it will expose (percentage answers, mandatory evidence refs). Author-independence and calibration are the difference between consulting IP and a product.
5. **Separate client evidence from product, then publish the methodology.** Strip the real-client layer (filenames included) into a private engagement workspace (Phase-5 design already anticipates this); then publish the archetype model + NHI taxonomy + scoring semantics as a short public methodology paper mapped to CSA/OWASP. Neutral credibility is your only marketing budget that compounds.

---

## (e) Sources consulted

**In-repo (primary artifacts inspected):** `README.md`; `HANDOFF.md`; `methodology/{METHODOLOGY,RUBRIC,PLAYBOOK,FACILITATOR-GUIDE,INSTRUMENT-REVIEW-METHODOLOGY}.md`; `methodology/{assessment-archetypes,archetype-questions,uc-archetype-map,bespoke-criteria}.csv`; `research/identity-taxonomy.md`; `research/use-cases.md`; `research/anz-current-state-evidence.md`; `research/iga/`; `research/vendors/` (19 profiles); `matrix/domains/{secrets,pam,iga}/` (use-cases, identity-catalog, evidence-catalog, current-state, regulatory-trace, vendor CSVs, built reports); `matrix/config/{vendor-ownership,vendor-residency,frameworks,data-provenance}.yaml`; `matrix/cross-domain-report.html`; `questionnaire/` + `app/src/` (rubric JSONs, `scoring.ts`); `presentation/{value-proposition,exec-summary}.html`; `PRD/PRD-FI-v0.1.md`; `docs/superpowers/MULTI-DOMAIN-ROADMAP.md`; `meta/instrument-review-2026-06-09.md` and `meta/iga-instrument-review-2026-06-10.md` (treated as author self-claims and independently re-checked where load-bearing). Verification runs: `python3 -m pytest -q` (308 passed), `python3 matrix/validate_data.py` (clean). (`meta/independent-audit-2026-06-11.md` noted as existing; not used to form this review.)

**Market/web (live research, 2026-06-11):**
- Palo Alto Networks completes CyberArk acquisition (closed 2026-02-11, ~$25B): [paloaltonetworks.com press release](https://www.paloaltonetworks.com/company/press/2026/palo-alto-networks-completes-acquisition-of-cyberark-to-secure-the-ai-era), [GovCon Wire](https://www.govconwire.com/articles/palo-alto-networks-cyberark-25b-acquisition)
- Delinea completes StrongDM acquisition (2026-03-05, agentic-AI rationale): [GlobeNewswire](https://www.globenewswire.com/news-release/2026/03/05/3250113/0/en/Delinea-Completes-StrongDM-Acquisition-to-Secure-AI-Agents-with-Continuous-Identity-Authorization.html), [Delinea](https://delinea.com/news/delinea-acquires-strongdm-to-secure-ai-with-continuous-authorization)
- Entro Security independence (no acquisition found): [PitchBook profile](https://pitchbook.com/profiles/company/522209-08), [Tracxn](https://tracxn.com/d/companies/entro-security/__ow0KJpYWuv5-XwJgpiI3SU1yJ0R6G_BGHdJpmnZJOhI)
- Gartner IAM Program Maturity Model / IT Score: [gartner.com 3993765](https://www.gartner.com/en/documents/3993765), [gartner.com 1203314](https://www.gartner.com/en/documents/1203314); Gartner IAM Summit 2025 themes: [Idenhaus recap](https://idenhaus.com/gartner-iam-summit-2025-recap/), [Cerbos recap](https://www.cerbos.dev/blog/gartner-iam-summit-2025-authorization-authzen-identity-security-expanding-to-every-workload)
- KuppingerCole IAM Maturity Assessment (50Q/17 capabilities, benchmarked): [kuppingercole.com](https://www.kuppingercole.com/advisory/iam-maturity-assessment)
- SailPoint Horizons maturity assessment + research: [sailpoint.com/horizons/assessment](https://www.sailpoint.com/horizons/assessment), [sailpoint.com identity-security-maturity](https://www.sailpoint.com/identity-security-maturity/)
- CyberArk Identity Security Maturity Model (ESG, 1,500 respondents) + Blueprint: [cyberark.com](https://www.cyberark.com/identity-security-maturity-model/)
- Delinea Identity Security Maturity Model: [delinea.com](https://delinea.com/solutions/identity-security-maturity-model)
- KPMG IAM Maturity Assessment (CMMI/COBIT-aligned): [kpmg.com](https://kpmg.com/hu/en/services/advisory/technology/cybersecurity/identity-and-access-management-services/iam-maturity-assessment.html)
- NHI market size/growth and 2025-26 consolidation: [MarketIntelo NHI market report](https://marketintelo.com/report/non-human-identity-management-market), [Security Boulevard — 9 enterprise identity trends 2026](https://securityboulevard.com/2026/05/9-enterprise-identity-trends-that-will-define-2026-and-beyond/), [GitGuardian — top NHI tools 2026](https://blog.gitguardian.com/nhi-security-tools/), [Cremit NHI platform comparison (RSAC 2026)](https://www.cremit.io/reports/rsac-2026-nhi)
- CSA agentic-AI identity guidance: [cloudsecurityalliance.org — Agentic AI IAM](https://cloudsecurityalliance.org/artifacts/agentic-ai-identity-and-access-management-a-new-approach), [CSA — State of NHI and AI Security](https://cloudsecurityalliance.org/artifacts/state-of-nhi-and-ai-security-survey-report)
- Oasis Security $120M Series B; Aembit Microsoft-ecosystem expansion: [Cremit/RSAC 2026 report](https://www.cremit.io/reports/rsac-2026-nhi), [Landbase IAM growth survey](https://www.landbase.com/blog/fastest-growing-identity-access-management)

*Reviewer note on independence: no memory/recall tooling was used; injected "prior observation" banners in tool output were disregarded. All market facts above were verified by live web research on the review date.*
