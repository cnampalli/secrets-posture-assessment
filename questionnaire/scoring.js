// Mirror of methodology/scoring.py — keep in lockstep via scoring-vectors.json.
function deriveState(questions, answers) {
  const vals = questions.map(q => [q.informs_state, answers[q.qid] ?? null]);
  if (vals.length && vals.every(([, v]) => v === "na")) return "NA";
  if (vals.some(([, v]) => v !== "yes" && v !== "no" && v !== "na")) return "PENDING";
  if (vals.some(([inf, v]) => inf === "GAP_PARTIAL" && v === "no")) return "GAP";
  if (vals.some(([inf, v]) => inf === "PARTIAL_MET" && v === "no")) return "PARTIAL";
  return "MET";
}
if (typeof module !== "undefined" && module.exports) module.exports = { deriveState };
