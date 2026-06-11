# How to Run a Posture Assessment — Facilitator Guide

**Who this is for:** anyone who can run a workshop. You do **not** need to be technical
and you do **not** need to understand the scoring engine. If you can book the right
people, ask questions, and keep a session on track, you can run this.

**The one thing to know up front:** you run the *conversation*; a **technical teammate**
runs the *four commands* that turn the conversation into the client's report. You don't
touch a command line. This guide tells you exactly when to pull them in.

> Going deeper later? `methodology/PLAYBOOK.md` is the full internal manual,
> `methodology/RUBRIC.md` explains the scoring, and `methodology/METHODOLOGY.md` is the
> version you can show the client. This guide is the plain-English "just run it" version.

---

## 1. What this is, and what you walk away with

You're assessing how well a client manages **secrets and machine identities** (API keys,
service accounts, certificates, tokens — the credentials software uses to talk to other
software). You walk through a fixed list of ~47 **use cases** (specific things a mature
organisation does), find out whether the client does each one, and score it.

At the end you hand the client **four things**:

| Artifact | What it is | File |
|---|---|---|
| **Gap report** | Interactive web page: every use case marked Met / Partial / Gap / Pending | `matrix/domains/secrets/secrets-report.html` |
| **Executive summary** | One-page web dashboard of the headline counts, for leadership | `exec-summary.html` |
| **Engagement menu / roadmap** | Prioritised to-do list of fixes — this is your follow-on sales wedge | `engagement-menu.json` |
| **Assessment record** | The official machine-readable record of every answer and score | `assessment-record.json` |

The first two open in any browser by double-clicking — no software, no internet. The
gaps in the report **are** the work you can propose next. That's the whole point.

---

## 2. Who you need in the room

Three roles. On a small engagement one person can wear two hats, but the roles are
distinct:

- **You — the facilitator.** Run the session, drive the questionnaire on screen, keep
  the conversation honest and moving. You own steps 1, 2, 3 and 6 below.

- **Your technical teammate.** Someone on your side who **knows secrets management** and
  is **comfortable running commands**. They help pick the framework (step 1), gut-check
  the scores (step 3), and run the four build commands (steps 4 and 5). You can be
  non-technical precisely because they aren't.

- **The client's stakeholders (their experts).** The people who actually know the
  answers:
  - **Compliance / risk** — needed in step 1 to confirm which regulations bind them.
  - **Engineering / platform / security** — needed in step 2; they know what the client
    *actually does* (not what the policy says it does).

Book real experts. The assessment is only as good as the honesty of the people answering.

---

## 3. Before the workshop — prep checklist

- [ ] **Confirm the client's industry and regulator** with their compliance contact, and
      agree which **preset** you'll measure against (see step 1 for the four choices).
- [ ] **Get a laptop ready** that has this project on it and can run Python. Your
      technical teammate confirms this — ask them to do a 5-minute dry run before the day.
- [ ] **Open the questionnaire once to check it loads:** double-click
      `questionnaire/questionnaire.html`. It should open in your browser with no errors and
      no internet needed. If it opens, you're ready.
- [ ] **Book the right client experts** for the right sessions (compliance for scoping,
      engineers for evidence). Plan for more than one session — 47 use cases is a lot to do
      well in one sitting.
- [ ] **Agree the ground rule with the client:** "If you're not sure, we leave it blank.
      We'd rather mark it *Pending* and come back than guess." Say this out loud at the start.

---

## 4. The six steps

Each step below tells you the **goal**, **who does what**, **exactly what to do**, and
**what "done" looks like**.

### Step 1 — Decide what you're measuring against

**Goal:** pick the rulebook the client must satisfy, so the report tests against the right
obligations.

**Who:** you + the client's compliance/risk contact + your technical teammate.

**What to do:** with the client's compliance contact, pick **one** preset that matches
their world:

| Preset | Use it for |
|---|---|
| `financial` | Banks, insurers, super funds — anyone regulated by APRA |
| `government` | Public-sector / government entities (PSPF / ISM regime) |
| `retail` | Retail and consumer businesses |
| `baseline` | Anyone who doesn't clearly fit the other three |

You don't have to remember anything technical here — you just **decide which word**
(`financial`, `government`, `retail`, or `baseline`) describes the client. Your teammate
plugs that word into the commands later. The Australian baseline (Essential 8 + Privacy
Act) is **always included automatically** — you never remove it.

**Done when:** you've written down one preset word, agreed with the client's compliance
person.

---

### Step 2 — Run the workshop and capture the answers

**Goal:** find out, honestly, what the client actually does for each use case.

**Who:** you (driving) + the client's engineers/security experts (answering).

**What to do:**

1. **Open** `questionnaire/questionnaire.html` in a browser and share your screen.
2. **Walk through each use case.** For each one the tool asks plain diagnostic
   questions — Do you do this? Everywhere or just some places? Is it enforced or just
   recommended? How often? Who owns it? Let the client's experts answer; **ask them to
   show you the proof** ("can you show me where that's configured?") rather than taking a
   yes at face value.
3. **When they don't know, leave it blank.** Don't guess and don't let them guess. A
   blank becomes a *Pending* — an honest "we need to check" — and that's a valid, useful
   result.
4. **Export at the end of every session.** Use the questionnaire's export button so
   nothing is lost. You can pause and resume across multiple meetings.

**Done when:** every in-scope use case has been walked through, and you've exported the
final answers. That export is the file `assessment-record.json` (your technical teammate
will recognise it).

> **Plain example:** One use case is "stop secrets from being committed into source code."
> If the client says "we have a tool that blocks it on every repository and alerts us," that's
> strong evidence. If they say "we tell developers not to, but nothing stops them," that's a
> gap — and you've just found a real finding.

---

### Step 3 — Settle the scores

**Goal:** turn the answers into a verdict for each use case: **Met**, **Partial**, **Gap**,
or **Pending**.

**Who:** you + your technical teammate (and the assessor — usually your teammate or a
senior reviewer makes the final call).

**What to do:** the tool does the first pass automatically — based on the answers, it
**proposes** a score for each use case. Then a human reviews each one and either:

- **agrees** with the proposed score, or
- **overrides** it — which is allowed and normal, because you often know more than the
  questions captured. **But every override must have a one-line reason and a confidence
  level** (High / Medium / Low). Never change a score silently. The reason is what makes
  the verdict defensible if the client's risk team or regulator questions it later.

**The four scores in plain English:**

| Score | Means |
|---|---|
| **Met** | They genuinely do this, properly and everywhere. |
| **Partial** | They do some of it, or only in some places, or it's not enforced. |
| **Gap** | They don't do it (or it's trivially bypassed). This is a finding. |
| **Pending** | Not enough evidence yet — come back to it. |

**Done when:** every use case has a final score, every override has a reason, and the
result is saved as `assessment-record.json`. This file is the official record everything
else is built from.

---

### Step 4 — Build the report

**Goal:** turn the saved answers into the client-readable gap report.

**Who:** your technical teammate runs this. You read the result.

**What to do:** hand your teammate the **technical hand-off pack** (section 5 below). They
run two commands. Out comes `matrix/domains/secrets/secrets-report.html` — an interactive page with five
tabs (the headline posture, a view per use case, a view per identity type, the compliance
mapping, and a full browse). You open it and **read off the scores**: Met / Partial / Gap /
Pending for each use case.

**Done when:** the report opens in a browser and shows the client's real scores (not a
blank template). The **Gap** and **Partial** rows are your raw material for step 5.

---

### Step 5 — Build the to-do list (the roadmap)

**Goal:** turn the gaps into a prioritised, sellable plan — what to fix first, why, and
what depends on what.

**Who:** your technical teammate runs this. You use the result with the client.

**What to do:** your teammate runs two more commands (in the hand-off pack). These produce:

- `engagement-menu.json` — the prioritised list of fixes, and
- `exec-summary.html` — the one-page leadership dashboard.

**How the prioritisation works (so you can explain it):** each gap is sorted on two simple
questions — *How risky is it?* (High / Med / Low) and *How hard is it to fix?* (High / Med /
Low). Crossing those gives four buckets:

- **Quick wins** — high risk, easy to fix → **do first**.
- **Major projects** — high risk, hard to fix → plan and resource these deliberately.
- **Fill-ins** — low risk, easy → bundle in opportunistically.
- **Hard slogs** — low risk, hard → defer unless a regulation forces it.

When two items tie, a binding regulation breaks the tie. The tool does this sorting
automatically.

**Done when:** you have the engagement menu and exec summary, and you can tell the client a
one-sentence story: "Here are your three quick wins to do now, and here's the one big
project everything else depends on."

> **Plain example:** "Block secrets in repositories" is high risk and easy to switch on →
> **quick win, do first.** "Build a live dashboard of secret sprawl" is also high risk, but
> it needs an inventory system stood up first → **major project, comes later.** Same risk,
> opposite ends of the plan — because one is easy and one has a dependency.

---

### Step 6 — Schedule the re-check

**Goal:** keep the assessment alive and prove that fixes actually worked.

**Who:** you, with the client.

**What to do:** agree a cadence before you leave:

1. **Re-run the whole assessment once a year** to catch drift and any new regulations.
2. **Re-run sooner if something big happens** — a security incident, a major architecture
   change, or a new regulation landing.
3. **Re-test each fix when it's done** to confirm the score actually moved (e.g. a Gap
   becoming Met). A fix isn't "closed" until the re-test proves it.

**Done when:** the client has a date for the next review and an agreement to re-test each
remediation as it lands. This is also your natural reason to come back — the recurring
engagement.

---

## 5. Technical hand-off pack (forward this to your technical teammate)

> **Facilitator:** you don't need to read this. Copy this whole section to your technical
> teammate. It assumes they have the project checked out and a terminal open **in the
> project root**.

**One-time setup (first run on a machine):**
```
pip install -r requirements.txt
```

**You'll be given one file from the workshop:** `assessment-record.json` (the questionnaire
export). Put it somewhere you can reference it; the commands below assume it's in the
project root. Replace `financial` with whichever preset the facilitator chose
(`financial` / `government` / `retail` / `baseline`).

**Run these four commands in order:**

```
# 1. Turn the workshop answers into the report's input file
python3 -m questionnaire.report_adapter assessment-record.json -o current-state.csv

# 2. Build the interactive gap report (writes to matrix/domains/secrets/secrets-report.html)
python3 matrix/build_matrix_viewer.py --preset financial --current-state current-state.csv

# 3. Build the prioritised engagement menu / roadmap
python3 -m questionnaire.roadmap_generator assessment-record.json -o engagement-menu.json --preset financial

# 4. Build the one-page executive summary
python3 -m presentation.build_exec_summary assessment-record.json -o exec-summary.html --preset financial --client "Client Name" --as-of "2026-06-03"
```

**What success looks like:**

| Command | You should see |
|---|---|
| 1 | A new `current-state.csv` created, one row per use case. |
| 2 | A printed line `Wrote .../secrets-report.html (N bytes)` plus counts of UCs/NHIs. Open the file in a browser — it shows the client's scores. |
| 3 | A new `engagement-menu.json` with the prioritised findings. |
| 4 | A new `exec-summary.html`. Open it — it shows the Met/Partial/Gap/Pending counts. |

**Notes:**
- `build_matrix_viewer.py` always writes to `matrix/domains/secrets/secrets-report.html` (no output flag) —
  if that file has uncommitted local changes, stash or back it up first.
- To compare against extra frameworks, add `--frameworks slug1,slug2` (valid slugs live in
  `matrix/domains/secrets/regulatory-trace.csv`: e.g. `apra-cps-234`, `asd-ism`, `cisa-ztmm-v2`,
  `essential-8`, `mitre-attack`).
- For finer per-finding tuning of the roadmap (override a risk band, record a dependency),
  pass `--engagement <csv>` to command 3 — see `PLAYBOOK.md` §5.

---

## 6. How to share the deliverable

- **Quickest:** email the single HTML files (`matrix/domains/secrets/secrets-report.html`,
  `exec-summary.html`). Each is self-contained — the recipient just double-clicks; no
  software, no internet.
- **Full package:** run `bash package.sh` to produce a zipped bundle (report + supporting
  docs) under `dist/`.
- **Need a PDF?** Open the HTML in a browser and use Print → Save as PDF.

---

## 7. Plain-English glossary

- **Use case (UC)** — one specific good practice you assess (there are ~47).
- **Archetype (A0–A8)** — a reusable scoring pattern behind a use case. You never touch
  these; the tool uses them to propose scores.
- **Met / Partial / Gap / Pending** — the four possible verdicts (see step 3).
- **Confidence (High / Med / Low)** — how strong the evidence behind a score is.
- **Preset** — the rulebook you measure against (`financial` / `government` / `retail` /
  `baseline`).
- **Overlay** — an extra framework layered on for comparison (optional).
- **Engagement menu** — the prioritised list of fixes; your follow-on proposal.

---

## 8. Where to go deeper

- `methodology/PLAYBOOK.md` — the full internal consultant manual (the authoritative
  procedure, with the reasoning behind each stage).
- `methodology/RUBRIC.md` — how scoring and the archetypes work.
- `methodology/METHODOLOGY.md` — the client-facing description of the method.
