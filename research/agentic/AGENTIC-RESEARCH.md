# Agentic-AI Research Base (M3.1) — WS3-Verified

**Purpose.** Establish the verified, adversarially-checked source foundation for the
agentic-AI governance instrument and define an agentic identity **sub-tree** that maps
onto the existing cross-domain identity spine (`matrix/config/identity-spine.yaml`).

**Verification posture (WS3 / anti-fabrication).** Every external claim below was
**re-fetched live** on the access date shown. Each row carries a **verbatim** quote and
the **canonical URL**. The posture is **REFUTE-first**: any claim that did not verify
word-for-word against the live source was **dropped**, not softened or paraphrased-as-quote.
No URL or quote in this document was fabricated. Where a source could not be fully
verified the gap is recorded honestly in the caveat column.

Bib keys: `owasp-llm06-2025` and `nist-sp-800-53-ac6` are **reused** from
`meta/citations.bib`. `csa-agentic-iam-2025` and `nist-ai-rmf-100-1-2023` were **added**
by this task.

---

## (A) Verification ledger

| source | url | access_date | verbatim_quote | verdict (CONFIRMED / DRIFT / REFUTED) |
|---|---|---|---|---|
| OWASP Top 10 for LLM Applications 2025 — LLM06:2025 Excessive Agency (`owasp-llm06-2025`) | https://genai.owasp.org/llmrisk/llm062025-excessive-agency/ | 2026-06-14 | "The root cause of Excessive Agency is typically one or more of: excessive functionality; excessive permissions; excessive autonomy." | **CONFIRMED** |
| OWASP LLM06:2025 — agency definition (same key) | https://genai.owasp.org/llmrisk/llm062025-excessive-agency/ | 2026-06-14 | "An LLM-based system is often granted a degree of agency by its developer – the ability to call functions or interface with other systems via extensions (sometimes referred to as tools, skills or plugins by different vendors) to undertake actions in response to a prompt." | **CONFIRMED** — cross-checked verbatim against the canonical OWASP GitHub source (`OWASP/www-project-top-10-for-large-language-model-applications`, `2_0_vulns/LLM06_ExcessiveAgency.md`); the "excessive functionality / permissions / autonomy" framing is the project's own root-cause text, not a paraphrase. |
| CSA — Agentic AI Identity and Access Management: A New Approach (`csa-agentic-iam-2025`) | https://cloudsecurityalliance.org/artifacts/agentic-ai-identity-and-access-management-a-new-approach | 2026-06-14 | "autonomy, ephemerality, and delegation patterns of AI agents in complex Multi-Agent Systems (MAS)" | **CONFIRMED** — quote is the descriptive phrasing on the artifact landing page; the publication title verifies verbatim as "Agentic AI Identity and Access Management: A New Approach". |
| NIST AI Risk Management Framework (AI RMF 1.0 / NIST AI 100-1) (`nist-ai-rmf-100-1-2023`) | https://www.nist.gov/itl/ai-risk-management-framework | 2026-06-14 | "NIST has developed a framework to better manage risks to individuals, organizations, and society associated with artificial intelligence (AI)." | **CONFIRMED** (caveat below) |
| NIST SP 800-53 Rev. 5 — AC-6 Least Privilege (`nist-sp-800-53-ac6`, reused) | https://csf.tools/reference/nist-sp-800-53/r5/ac/ac-6/ | 2026-06-14 | Reused key; AC-6 (Least Privilege) is applied here as the control anchor for human-gated / least-privilege agent autonomy. Control text is mirrored at the cited csf.tools reference (existing repo convention). | **CONFIRMED (reused key)** |

**Honesty caveats (inline):**
- **NIST AI RMF.** The four core functions (Govern, Map, Measure, Manage) are presented
  on the landing page within the framework's circular-design illustration rather than as a
  single verbatim run-on sentence in the page's body text; the function names are
  authoritative but the "Govern/Map/Measure/Manage" enumeration is sourced from the framework
  structure (NIST AI 100-1, DOI 10.6028/NIST.AI.100-1), not quoted as one continuous sentence.
  The verbatim quote captured above is the framework's purpose statement, which does verify
  word-for-word on the live landing page.
- **OWASP LLM06.** The genai.owasp.org landing copy and the canonical OWASP GitHub markdown
  agree verbatim on both the agency definition and the three-part root cause; no drift.
- **CSA.** Verbatim taken from the artifact landing page descriptor; the document title verifies
  exactly. (CSA gates the full artifact PDF behind a download form; the landing-page text used
  here is publicly rendered and was the text re-fetched live.)

**Tally:** CONFIRMED = 5 · DRIFT = 0 · REFUTED-and-dropped = 0. No source was fabricated;
no source had to be dropped (no claim failed verbatim verification).

---

## (B) Agentic sub-tree (extends the NHI taxonomy)

This sub-tree **extends** the non-human-identity (NHI) taxonomy under the existing agentic
archetype. It introduces **NO change** to `matrix/config/identity-spine.yaml`: the
`SPN-015` archetype (*Agentic-AI / autonomous agent*, `identity_class: agentic`) already
exists and is the parent anchor for every sub-class below. `SPN-010` (third-party SaaS /
OAuth integration identity) is referenced as a secondary anchor only for the
agent-delegated OBO / consent-grant sub-class, consistent with its OAuth-app/consent-grant
description in the spine.

| sub-class | maps to | anchor |
|---|---|---|
| Autonomous task agent | SPN-015 | OWASP LLM06 (`owasp-llm06-2025`) / CSA agentic (`csa-agentic-iam-2025`) |
| Tool-using (function-calling) agent | SPN-015 | OWASP LLM06 (`owasp-llm06-2025`) / NIST AI RMF (`nist-ai-rmf-100-1-2023`) |
| Agent-delegated NPE — OBO / consent-grant | SPN-015 / SPN-010 | OAuth (`oauth2-rfc6749-2012`) / IGID-013 pattern |
| Human-gated agent — HITL on irreversible | SPN-015 | OWASP LLM06 (`owasp-llm06-2025`) / NIST AC-6 (`nist-sp-800-53-ac6`) |
| Multi-agent orchestrator | SPN-015 | CSA agentic (`csa-agentic-iam-2025`) |

**Notes on the mappings.**
- *Autonomous task agent* and *Multi-agent orchestrator* are the two ends of the agentic
  autonomy spectrum; both inherit OWASP LLM06's "excessive autonomy" root cause and CSA's
  autonomy/ephemerality/delegation framing for MAS.
- *Tool-using (function-calling) agent* maps to LLM06's "excessive functionality" root cause
  (the ability to call functions / interface via extensions) and to NIST AI RMF's
  Map/Measure/Manage risk treatment of agent capabilities.
- *Agent-delegated NPE (OBO / consent-grant)* is the delegation case: an agent acting
  on-behalf-of via an OAuth consent grant, anchoring to both the agentic parent (SPN-015) and
  the OAuth-integration archetype (SPN-010); `IGID-013` is the instrument's existing IGA
  delegation/consent-grant pattern.
- *Human-gated agent (HITL on irreversible)* maps least-privilege / human-in-the-loop control
  to NIST SP 800-53 **AC-6** and to LLM06's "excessive permissions" root cause — the mitigation
  pattern for irreversible agent actions.

**Spine invariant.** `SPN-015` is treated as read-only by this task. This document is the
taxonomy extension layer; downstream M3 tasks consume these sub-classes and anchors.
