# Posture Assessment — Consultant Operating Manual (Playbook)

**Status:** Draft
**Date:** 2026-05-30
**Audience:** Internal — the consultant running an engagement.
**Companion (client-facing):** `methodology/METHODOLOGY.md`
**Builds on:** WS-1 rubric (`RUBRIC.md`), WS-2 regulatory overlay (`matrix/config/`), WS-3 questionnaire (`questionnaire/`), report adapter (ADR-011).

This is the repeatable procedure for running a posture-assessment engagement end-to-end
for any AU client in any industry. The GAP/PARTIAL findings it produces are the engagement
menu — the consulting wedge. The procedure below is client-agnostic; **worked-example
callouts** (marked `> **XYZ example**`) ground each stage in the real XYZ secrets-management
assessment.

## The engagement lifecycle (6 stages)

1. **Scope** — pick the regulatory overlay(s) for the client/industry.
2. **Collect evidence** — run the questionnaire instrument (facilitated).
3. **Score** — rubric-assisted state, assessor confirms/overrides with rationale + confidence.
4. **Report current state** — project answers into the matrix gap report.
5. **Build the remediation roadmap** — turn GAP/PARTIAL into the prioritised engagement menu.
6. **Re-assess** — annual baseline + event-triggered + per-finding re-test.

Each stage below: **Purpose → Procedure → Tooling → Outputs → XYZ example.**

---

## Stage 1 — Scope

**Purpose.** Select the binding framework(s) so the assessment scopes precisely to what the
client must satisfy. The scope decision is load-bearing for everything downstream: it
determines which obligations the gap report tests against, and therefore which GAP/PARTIAL
findings become the engagement menu. Scope too narrowly and you miss obligations the client
is exposed to; scope too broadly and you dilute the assessment with controls that do not bind
this client. The goal is the smallest framework set that fully covers the client's regulatory
exposure, plus a small number of comparison overlays that sharpen the narrative.

**Procedure.**

1. **Identify the client's industry and binding obligations.** Establish who regulates the
   client, what sector they operate in, and which standards they are contractually or legally
   required to meet. This is a fact-finding step done with the client's compliance and risk
   stakeholders, not an assumption — confirm the obligations rather than inferring them from
   the industry label alone.
2. **Choose the matching preset.** Map the client to exactly one primary preset in
   `matrix/config/presets/`: `financial.yaml` for financial institutions under APRA,
   `government.yaml` for public-sector entities under the PSPF/ISM regime, `retail.yaml` for
   retail and consumer businesses, or `baseline.yaml` when none of the sector presets is a
   clean fit. The primary preset is the spine of the scope.
3. **Add 1–2 comparison overlays.** Layer one or two additional framework overlays on top of
   the primary preset to give the client a reference point — for example, comparing against a
   stricter sector's expectations, or against a framework the client is considering adopting.
   Keep this to one or two; more overlays add noise without adding insight.
4. **Confirm the always-on AU baseline.** Regardless of preset, confirm that the ASD
   **Essential 8** and the **Privacy Act** remain in scope as the always-on Australian
   baseline. Every AU client inherits these; they are never removed from scope, only layered
   under the sector-specific obligations.

**Tooling.** The presets live in `matrix/config/presets/*.yaml` and the framework
definitions they reference live in `matrix/config/frameworks.yaml`. The matrix build (WS-2)
consumes the selected preset and overlays to produce the scoped framework set — the consultant
selects; the build applies the selection mechanically.

**Outputs.** The scoped framework set for the engagement: one primary preset, the always-on AU
baseline, and any comparison overlays. This set is the contract the gap report tests against
in Stage 4.

> **XYZ example**
> XYZ is an AU Tier-1 financial institution, so the scope uses the `financial.yaml` preset
> (APRA CPS 234 / CPS 230 plus the ASD ISM), with the **Essential 8** baseline always-on. No
> additional comparison overlay was needed — the FI obligations plus the AU baseline fully
> covered the secrets-management exposure under assessment.

---

## Stage 2 — Collect evidence

**Purpose.** Gather the evidence that answers each use-case's diagnostic questions. The
assessment is only as good as the evidence behind it, so this stage is about getting honest,
specific answers to the per-use-case items — not about scoring (that comes next). The
consultant's job here is to elicit what the client actually does, with enough detail that the
rubric can propose a defensible state in Stage 3.

**Procedure.**

1. **Open the questionnaire instrument.** Open `questionnaire/questionnaire.html` directly in a
   browser. It is fully self-contained — no server, no install, no network dependency — so it
   runs on a consultant laptop in a client meeting room or share-screen session without any
   setup.
2. **Facilitate live with the client.** Run the questionnaire as a facilitated session: the
   consultant drives the instrument and asks the questions, while the client's subject-matter
   experts supply the answers and evidence. Facilitating live keeps the answers grounded —
   the consultant can probe, ask for the underlying artifact, and avoid the optimistic
   self-assessment that an unattended form invites.
3. **Answer each use-case's items.** Work through every in-scope use-case, answering each of
   its diagnostic items against the dimensions the rubric cares about (coverage, enforcement,
   exceptions, cadence, depth, governance). Where the client cannot answer an item, leave it
   un-answered rather than guessing — an honest gap in evidence is itself a signal and feeds
   the PENDING state downstream.
4. **Autosave and export progress.** The questionnaire holds answered items in its working
   state and supports export, so a session can be paused and resumed and the partial record
   preserved. Export at the end of each session so progress is never lost between meetings.

**Tooling.** `questionnaire/questionnaire.html` is the built, self-contained artifact. It is
generated by `questionnaire/build_questionnaire.py` from the WS-1 rubric, so the questions the
consultant asks are exactly the archetype diagnostic questions defined in the rubric — the
instrument and the scoring model stay in lockstep.

**Outputs.** Answered items per use-case, held in the questionnaire's working state (and
exported between sessions). These answers are the raw input the rubric scores in Stage 3.

> **XYZ example**
> All 47 use-cases were walked through in facilitated sessions. The two seed findings were
> answered against the 2019 red-team evidence: **UC-F-001** (secret push-protection not
> deployed in blocking mode across repositories) and **UC-N-001** (the plaintext-secret-sprawl
> KPI dashboard not in operational use). In both cases the lived-experience evidence from the
> red team grounded the answers rather than relying on attested self-assessment.

---

## Stage 3 — Score

**Purpose.** Convert the gathered answers into a defensible MET / PARTIAL / GAP / PENDING state
for each use-case. Scoring is where evidence becomes a verdict — and the verdict has to survive
scrutiny from the client's risk function and, ultimately, their regulator. The rubric does the
mechanical first pass; the assessor owns the final call. This stage produces the record that
every later stage builds on.

**Procedure.**

1. **The rubric proposes a state.** For each use-case, the rubric maps the answers onto the
   use-case's archetype (A0–A8) and proposes a state mechanically from the archetype's MET /
   PARTIAL / GAP definitions and the load-bearing dimensions those definitions specify. This
   proposed state is a starting point, not a verdict — it is derived purely from the answers as
   recorded.
2. **The assessor confirms or overrides.** The assessor reviews each proposed state and either
   confirms it or **overrides** it. An override is legitimate — the assessor often knows more
   than the answers captured — but it is never silent: every override must carry a **rationale**
   citing the dimension(s) where the assessor's read differs from the rubric's, plus a
   **confidence** level reflecting the strength of the underlying evidence. The rubric is a
   forcing function for explicit documentation, not an authority that overrides domain
   expertise.
3. **Export the assessment record.** Export the scored result as `assessment-record.json`
   (schema `posture-assessment-record/v1`). This is the canonical, machine-readable record of
   the assessment and the hand-off point into Stage 4's reporting.

**Tooling.** `methodology/RUBRIC.md` defines the archetype model, the state-derivation rule,
the confidence axis, and the override protocol; `methodology/assessment-archetypes.csv` is the
archetype library the rubric maps onto; `methodology/scoring.py` implements the mechanical
state proposal; and the questionnaire's export produces the `assessment-record.json` document.

**Outputs.** `assessment-record.json` — a per-use-case record carrying `final_state`,
`proposed_state`, `confidence`, and `rationale`, so every verdict is traceable back to both the
rubric's mechanical proposal and the assessor's recorded judgment.

> **XYZ example**
> Dogfooding the rubric against the frozen expert verdicts reproduced **46 of 47** judgments
> mechanically. The single divergence was a principled assessor override — **UC-N-012**, moved
> from PENDING to GAP — logged with its rationale. That one override is exactly the documented,
> defensible divergence the protocol is designed to capture, rather than a silent disagreement
> with the rubric.
