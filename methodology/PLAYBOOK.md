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
4. **Preserve and export progress.** The questionnaire holds answered items in its working
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
   use-case's archetype(s) (A0–A8) and proposes a state mechanically from the archetype's MET /
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

---

## Stage 4 — Report current state

**Purpose.** Render the scored assessment record as the client-readable gap report. Stage 3
produces a canonical, machine-readable verdict; Stage 4 turns that verdict into the artifact
the client actually reads — the matrix gap report — scoped to the current-state column so the
client sees, use-case by use-case, exactly where they stand against the framework set selected
in Stage 1. Nothing new is decided here; this stage is a faithful projection of the record into
the reporting surface.

**Procedure.**

1. **Project the record to the report CSV.** Run the report adapter to project
   `assessment-record.json` into the flat current-state CSV the report consumes:

   ```
   python3 -m questionnaire.report_adapter <record.json> -o current-state.csv
   ```

   The adapter is a pure projection — it reads the record's per-use-case `final_state` and
   carries it into the CSV without re-deriving or re-interpreting anything.
2. **Build the report scoped to current state.** Render the matrix viewer against that CSV so
   the report reflects the assessed current state rather than a blank template:

   ```
   python3 matrix/build_matrix_viewer.py --current-state current-state.csv
   ```

3. **Read off the per-use-case states.** Walk the rendered report and read off the
   MET / PARTIAL / GAP / PENDING verdict for each use-case. GAP and PARTIAL rows are the
   findings that feed the remediation roadmap in Stage 5; PENDING rows flag where evidence was
   insufficient and a re-visit is owed.

**Tooling.** `questionnaire/report_adapter.py` projects the record into the report CSV;
`matrix/build_matrix_viewer.py` renders the matrix gap report and accepts the `--current-state`
flag to scope the report to the assessed current state.

**Outputs.** The matrix gap report — the client-readable, current-state-scoped view of every
use-case's verdict against the selected framework set.

> **XYZ example**
> Of the 47 use-cases assessed, the report rendered **0 MET, 16 PARTIAL, 11 GAP, and 20
> PENDING**. The headline gap is the absent NHI inventory layer above the vault tier: Vault
> Enterprise was selected in 2019, but the layer that would give adoption coverage,
> observability, and ownership-attestation above the vault never followed — so adoption and
> attestation lag the tooling, and the report surfaces that as a structural gap rather than a
> point failure.

---

## Stage 5 — Build the remediation roadmap

**Purpose.** Turn the GAP and PARTIAL findings from Stage 4 into a sequenced, defensible
engagement menu — the consulting wedge. A flat list of gaps is not a roadmap; the client needs
to know what to do first, why, and what each item depends on. This stage applies a consistent
prioritisation method so the ordering survives challenge from the client's risk function and
maps cleanly onto a proposable engagement.

**Procedure — the prioritisation method.** Each GAP/PARTIAL finding is placed on two
qualitative axes and dropped into a quadrant. The method deliberately uses **bands, not numeric
scores**: a banded, anchor-driven call is more honest and more defensible than a false-precision
number, and it forces the consultant to name the reasoning rather than hide it in a weighting.

- **Axis 1 — Risk / exposure → High / Med / Low.** Band each finding from qualitative anchors:
  the residual exposure that remains given current controls, the blast radius if it were
  exploited (how many NHIs and downstream systems it touches), and — decisively — whether it is
  an *active* exposure rather than a latent weakness. An active exposure (for example, plaintext
  secrets already present in repositories) bands **High** because the exposure is live, not
  hypothetical. No numeric score is computed.
- **Axis 2 — Remediation effort → High / Med / Low.** Band each finding from effort anchors:
  the dependency depth (does it need the inventory layer or another finding closed first?),
  whether closing it requires organisational or process change versus a pure configuration
  change, and how much of the work is already covered by tooling the client owns. Where the
  selected tooling already exists (Vault was selected in 2019), the effort to exploit it bands
  **lower** than a finding that needs net-new capability.
- **Quadrants.** Crossing the two axes yields four quadrants that order the menu:
  **Quick wins** (High risk / Low effort — do first), **Major projects** (High risk / High
  effort — scope and sequence deliberately), **Fill-ins** (Low risk / Low effort — bundle
  opportunistically), and **Hard slogs** (Low risk / High effort — defer unless a regulatory
  driver pulls them forward).
- **Regulatory tie-breaker / escalator.** A binding regulatory obligation (APRA CPS 234 / CPS
  230, the ASD ISM, or the selected overlay) is used two ways: it **breaks ties** between
  findings that land in the same cell, and it can **escalate a finding's risk band up by one**
  where the obligation makes the exposure non-discretionary. This is **always logged with the
  specific control reference, never applied silently** — an escalation without a cited control
  is not permitted, because the client must be able to trace why a finding moved.
- **Dependency note.** Every row records its sequencing constraints — for example, the
  inventory layer must exist before ownership-attestation findings can be closed — so the
  resulting roadmap is actually buildable in order rather than being an unordered wish-list.

**Engagement-menu row shape.** Each finding becomes one row of the engagement menu with this
shape:

```
UC-id · state · risk band · effort band · quadrant · regulatory driver · dependency · proposed engagement
```

**Tooling.** This stage currently **documents** the prioritisation method; it is applied by the
consultant against the Stage 4 report. The generator that auto-emits the engagement menu
directly from `assessment-record.json` is a later WS-4 slice — until then the method here is the
authority and the menu is produced by hand following it.

**Outputs.** The prioritised engagement menu — the ordered, dependency-aware set of
GAP/PARTIAL findings, each banded and tied to its regulatory driver and proposed engagement.
This menu is the wedge.

> **XYZ example**
> Two findings show the method end-to-end. **UC-F-001** (secret push-protection not deployed in
> blocking mode across repositories) is an *active* plaintext-secret exposure → **High risk**,
> and it is deployable as blocking-mode configuration on the existing repositories → **Low
> effort**, landing it in **Quick wins** — do first. **UC-N-001** (the plaintext-secret-sprawl
> KPI dashboard not in operational use) is also **High risk**, but it depends on the absent NHI
> inventory layer to source its data → **High effort**, landing it in **Major projects** with a
> recorded dependency: the inventory layer must be stood up first. The two findings carry equal
> risk yet sort to opposite ends of the roadmap purely on effort and dependency — which is the
> point of the method.

---

## Stage 6 — Re-assess

**Purpose.** Keep the posture current and measure remediation progress over time. A posture
assessment is a point-in-time snapshot; without re-assessment it decays as the environment,
the threats, and the obligations change, and the client has no way to prove that the
remediation work actually moved their state. This stage defines the cadence that keeps the
assessment a living instrument and produces the deltas that demonstrate progress.

**Procedure / cadence.**

1. **Annual baseline re-assessment.** Re-run the full assessment on an annual cadence to
   refresh every use-case's state, catch drift, and re-baseline against any framework changes.
   This is the standing rhythm that keeps the posture from going stale.
2. **Event-triggered re-assessment.** Re-assess out of cycle when a triggering event occurs:
   a post-incident review, a major architecture change, or a new regulatory obligation entering
   scope. Each of these can invalidate prior verdicts, so the assessment is refreshed in
   response rather than waiting for the annual cycle.
3. **Per-finding re-test.** After each remediation closes, re-test that specific finding to
   confirm its state actually moved — for example GAP → PARTIAL → MET. The re-test is the
   evidence that a remediation worked; a finding is not considered closed until its re-test
   confirms the state transition.

**Outputs.** A cadence schedule (annual baseline plus event triggers) and the assessment deltas
between runs — the per-use-case state changes that show, finding by finding, how the posture
moved since the last assessment.

> **XYZ example**
> After the push-protection rollout, **UC-F-001** is re-tested to confirm the state moved
> **GAP → MET** — closing the loop on the Quick-win that opened the engagement menu, and giving
> the client documented evidence that the first remediation landed.
