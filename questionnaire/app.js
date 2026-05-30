/* Variant-A wizard. Engine: deriveState() (inlined from scoring.js).
   Rich record is the single source of truth; autosaved to localStorage. */
const STORE_KEY = "posture-assessment-record/v1";
const SCHEMA = "posture-assessment-record/v1";
const STATES = ["GAP", "PARTIAL", "MET", "PENDING", "NA"];
const RUBRIC_BY_ID = Object.fromEntries(RUBRIC.map(u => [u.uc_id, u]));

// responses[uc_id] = {answers:{}, overridden:bool, final_state:str|null, rationale:str, confidence:str}
let responses = {};
let current = RUBRIC[0] ? RUBRIC[0].uc_id : null;
const uiOpen = {};

function blankResponse() { return {answers: {}, overridden: false, final_state: null, rationale: "", confidence: "MED"}; }
function resp(id) { return (responses[id] = responses[id] || blankResponse()); }

function loadSaved() {
  try {
    const raw = localStorage.getItem(STORE_KEY);
    if (raw) { const rec = JSON.parse(raw); if (rec && rec.responses) responses = rec.responses; }
  } catch (e) { /* ignore corrupt autosave */ }
}
function save() {
  try { localStorage.setItem(STORE_KEY, JSON.stringify(buildRecord())); }
  catch (e) { toast("Autosave unavailable"); }
}

function proposedFor(uc) {
  if (uc.kind === "bespoke") return null;          // A0 manual
  return deriveState(uc.questions, resp(uc.uc_id).answers);
}
function finalFor(uc) {
  const r = resp(uc.uc_id);
  if (r.overridden && r.final_state) return r.final_state;
  const p = proposedFor(uc);
  return p || r.final_state || "PENDING";
}
function whyFor(uc) {
  const r = resp(uc.uc_id);
  if (uc.kind === "bespoke") return "Bespoke (A0) — assessor sets the state from the criteria below";
  const p = proposedFor(uc), a = r.answers, qs = uc.questions;
  if (p === "PENDING") { const n = qs.filter(q => !["yes","no","na"].includes(a[q.qid])).length; return n + " of " + qs.length + " question(s) unanswered"; }
  if (p === "NA") return "All criteria marked not-applicable";
  if (p === "GAP") { const q = qs.find(q => q.informs_state === "GAP_PARTIAL" && a[q.qid] === "no"); return "GAP↔PARTIAL question is No (" + q.qid + ", " + q.dimension + ")"; }
  if (p === "PARTIAL") { const q = qs.find(q => q.informs_state === "PARTIAL_MET" && a[q.qid] === "no"); return "A PARTIAL↔MET question is No (" + q.qid + ", " + q.dimension + ")"; }
  return "All criteria satisfied across every dimension";
}

function buildRecord() {
  const out = {schema: SCHEMA, generated: new Date().toISOString(), responses: {}};
  RUBRIC.forEach(uc => {
    const r = responses[uc.uc_id]; if (!r) return;
    out.responses[uc.uc_id] = {
      archetype: uc.archetype, answers: r.answers,
      proposed_state: proposedFor(uc), final_state: finalFor(uc),
      overridden: !!r.overridden, rationale: r.rationale || "", confidence: r.confidence || "MED"
    };
  });
  return out;
}

/* ---- rendering ---- */
function renderRail() {
  const groups = {};
  RUBRIC.forEach(u => (groups[u.category] = groups[u.category] || []).push(u));
  let h = "";
  for (const g in groups) {
    h += '<div class="rail-grp">' + g + "</div>";
    groups[g].forEach(u => {
      h += '<div class="rail-item ' + (u.uc_id === current ? "active" : "") + '" onclick="App.go(\'' + u.uc_id + '\')">' +
        '<span class="dot ' + finalFor(u) + '"></span><span class="t">' + esc(u.title) + '</span>' +
        '<span class="mono">' + u.uc_id + "</span></div>";
    });
  }
  document.getElementById("rail").innerHTML = h;
  const scored = RUBRIC.filter(u => { const p = proposedFor(u); const r = responses[u.uc_id];
    return (p && p !== "PENDING") || (u.kind === "bespoke" && r && r.final_state); }).length;
  document.getElementById("progress").textContent = scored + " / " + RUBRIC.length + " scored";
}

function renderMain() {
  const uc = RUBRIC_BY_ID[current]; if (!uc) return;
  const r = resp(uc.uc_id);
  let h = '<div class="crumb">' + uc.category + " · use case</div>" +
    '<div class="uc-head"><h2>' + esc(uc.title) + '</h2><span class="arch-badge mono">' + uc.archetype + " · " + esc(uc.archetype_name) + "</span></div>" +
    '<div class="uc-sub mono">' + uc.uc_id + "</div>";

  if (uc.kind === "bespoke") {
    h += '<div class="bespoke"><div class="qmeta"><span class="pill">bespoke criteria (A0) — guidance</span></div>';
    uc.sub_criteria.forEach(sc => {
      const on = r.answers[sc.sub_id] === true;
      h += '<label><input type="checkbox" ' + (on ? "checked" : "") + ' onchange="App.check(\'' + sc.sub_id + '\',this.checked)">' +
        "<span>" + esc(sc.sub_criterion) + "<div class=\"ev\">" + esc(sc.question) + " — <i>" + esc(sc.evidence) + "</i></div></span></label>";
    });
    h += "</div>";
  } else {
    uc.questions.forEach(q => {
      const a = r.answers[q.qid] || "";
      h += '<div class="q"><div class="qmeta"><span class="pill">' + q.dimension + '</span><span class="pill ' +
        (q.informs_state === "GAP_PARTIAL" ? "gp" : "pm") + '">' + (q.informs_state === "GAP_PARTIAL" ? "GAP ↔ PARTIAL" : "PARTIAL ↔ MET") + "</span></div>" +
        "<p>" + esc(q.text) + "</p><div class=\"seg\">" +
        ["yes", "no", "na"].map(v => '<button data-v="' + v + '" class="' + (a === v ? "on" : "") + '" onclick="App.answer(\'' + q.qid + '\',\'' + v + '\')">' + v.toUpperCase() + "</button>").join("") +
        "</div></div>";
    });
  }

  const proposed = proposedFor(uc), final = finalFor(uc);
  h += '<div class="score"><div class="score-row">' +
    '<span class="state-chip ' + final + '">' + final + "</span>" +
    '<span class="why"><b>' + (uc.kind === "bespoke" ? "State." : "Proposed.") + "</b> " + whyFor(uc) + "</span>" +
    '<span class="ovr-toggle" onclick="App.toggleOvr()">' + (uiOpen[uc.uc_id] ? "▾ hide" : "▸ override / confidence") + "</span></div>" +
    '<div class="ovr ' + (uiOpen[uc.uc_id] ? "open" : "") + '">' +
    "<label>" + (uc.kind === "bespoke" ? "Rationale" : "Override rationale (required to change the proposed state)") + "</label>" +
    '<textarea id="rat" oninput="App.setRationale(this.value)">' + esc(r.rationale) + "</textarea>" +
    '<div class="ovr-grid"><div><label>Confidence</label><div class="conf">' +
    ["LOW", "MED", "HIGH"].map(c => '<button class="' + (r.confidence === c ? "on" : "") + '" onclick="App.setConf(\'' + c + '\')">' + c + "</button>").join("") +
    "</div></div><div><label>Final state</label> " +
    '<select onchange="App.setFinal(this.value)"><option value="">' + (proposed ? "(proposed: " + proposed + ")" : "(choose)") + "</option>" +
    STATES.map(s => '<option value="' + s + '" ' + (r.final_state === s ? "selected" : "") + ">" + s + "</option>").join("") +
    "</select></div></div></div></div>";

  const idx = RUBRIC.findIndex(u => u.uc_id === current);
  h += '<div class="navrow"><button class="btn ghost" ' + (idx === 0 ? "disabled" : "") +
    ' onclick="App.go(RUBRIC[' + (idx - 1) + ']&&RUBRIC[' + (idx - 1) + '].uc_id)">← Previous</button>' +
    '<button class="btn" onclick="App.go(RUBRIC[' + (idx + 1) + ']&&RUBRIC[' + (idx + 1) + '].uc_id)">Save &amp; next →</button></div>';
  document.getElementById("main").innerHTML = h;
}

function render() { renderRail(); renderMain(); }
function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, c => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}[c])); }
function toast(m) { const t = document.getElementById("toast"); t.textContent = m; t.classList.add("show"); setTimeout(() => t.classList.remove("show"), 1600); }

const App = {
  go(id) { if (id) { current = id; render(); window.scrollTo(0, 0); } },
  answer(qid, v) { const a = resp(current).answers; a[qid] = (a[qid] === v ? undefined : v); if (a[qid] === undefined) delete a[qid]; save(); render(); },
  check(sid, on) { resp(current).answers[sid] = on; save(); renderRail(); },
  toggleOvr() { uiOpen[current] = !uiOpen[current]; renderMain(); },
  setRationale(v) { resp(current).rationale = v; save(); },
  setConf(c) { resp(current).confidence = c; save(); renderMain(); },
  setFinal(v) {
    const uc = RUBRIC_BY_ID[current], r = resp(current);
    if (!v) { r.overridden = false; r.final_state = null; save(); render(); return; }
    const proposed = proposedFor(uc);
    if (proposed && v !== proposed && !(r.rationale || "").trim()) {
      uiOpen[current] = true; renderMain();
      const ta = document.getElementById("rat"); if (ta) ta.classList.add("need");
      toast("Rationale required to override"); return;
    }
    r.overridden = uc.kind === "bespoke" ? true : (v !== proposed);
    r.final_state = v; save(); render();
  },
  exportRecord() {
    const blob = new Blob([JSON.stringify(buildRecord(), null, 2)], {type: "application/json"});
    const a = document.createElement("a"); a.href = URL.createObjectURL(blob);
    a.download = "assessment-record.json"; a.click(); toast("Record exported");
  },
  importRecord(text) {
    let rec; try { rec = JSON.parse(text); } catch (e) { toast("Import failed: invalid JSON"); return; }
    if (!rec || rec.schema !== SCHEMA) { toast("Import failed: unrecognised schema"); return; }
    const incoming = rec.responses || {};
    Object.keys(incoming).forEach(id => {
      if (!RUBRIC_BY_ID[id]) return;
      const s = incoming[id];
      responses[id] = {answers: s.answers || {}, overridden: !!s.overridden,
        final_state: s.final_state || null, rationale: s.rationale || "", confidence: s.confidence || "MED"};
    });
    save(); render(); toast("Record imported");
  }
};

document.getElementById("importFile").addEventListener("change", e => {
  const f = e.target.files[0]; if (!f) return;
  const rd = new FileReader(); rd.onload = () => App.importRecord(rd.result); rd.readAsText(f); e.target.value = "";
});

loadSaved();
render();
