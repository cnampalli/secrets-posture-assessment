// exec-summary.js — interactive exec-summary view. Dual-mode: plain browser
// script + Node-importable pure helpers (mirrors questionnaire/scoring.js).

const QUADRANTS = ["Quick wins", "Major projects", "Fill-ins", "Hard slogs"];
const RISK_RANK = { High: 0, Med: 1, Low: 2 };
const EFFORT_RANK = { Low: 0, Med: 1, High: 2 };

function groupByQuadrant(items) {
  const groups = {};
  for (const q of QUADRANTS) groups[q] = [];
  for (const it of items) (groups[it.quadrant] || (groups[it.quadrant] = [])).push(it);
  return groups;
}

function sortItems(items, key) {
  const field = key === "effort" ? "effort_band" : "risk_band";
  const rank = key === "effort" ? EFFORT_RANK : RISK_RANK;
  return [...items].sort((a, b) =>
    ((rank[a[field]] ?? 9) - (rank[b[field]] ?? 9)) || a.uc_id.localeCompare(b.uc_id));
}

function filterItems(items, opts) {
  const { quadrant = null, state = null } = opts || {};
  return items.filter(it =>
    (!quadrant || it.quadrant === quadrant) && (!state || it.state === state));
}

// ---------------------------------------------------------------------------
// Browser-only interactive UI. Guarded so Node can eval the pure helpers above
// without ever touching `document`.
// ---------------------------------------------------------------------------
if (typeof document !== "undefined") {
  const SNAPSHOT_STATES = [
    { key: "MET", label: "Met", cls: "state-met" },
    { key: "PARTIAL", label: "Partial", cls: "state-partial" },
    { key: "GAP", label: "Gap", cls: "state-gap" },
    { key: "PENDING", label: "Pending", cls: "state-pending" },
  ];
  const STATE_CLASS = {
    MET: "state-met", PARTIAL: "state-partial", GAP: "state-gap", PENDING: "state-pending",
  };
  const TIER_QUADRANTS = ["Quick wins", "Major projects"];

  const reduceMotion =
    typeof window.matchMedia === "function" &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // --- tiny DOM helpers (textContent-only for data; never innerHTML) ---
  function el(tag, opts) {
    const node = document.createElement(tag);
    if (!opts) return node;
    if (opts.class) node.className = opts.class;
    if (opts.text != null) node.textContent = String(opts.text);
    if (opts.attrs) for (const [k, v] of Object.entries(opts.attrs)) node.setAttribute(k, v);
    if (opts.children) for (const c of opts.children) if (c) node.appendChild(c);
    return node;
  }
  function mount(id) {
    const node = document.getElementById(id);
    if (node) node.textContent = "";
    return node;
  }
  function chip(text, cls) {
    return el("span", { class: "es-chip" + (cls ? " " + cls : ""), text });
  }
  function firstDriver(item) {
    const d = item.regulatory_driver;
    return Array.isArray(d) && d.length ? d[0] : null;
  }
  function driverLabel(d) {
    if (!d) return "";
    const code = d.control_code || "";
    const fw = d.framework_slug || "";
    return fw && code ? `${fw} · ${code}` : code || fw;
  }

  const DATA = (typeof window !== "undefined" && window.__EXEC_DATA__) || {};
  const snapshot = DATA.snapshot || {};
  const meta = DATA.meta || {};
  const items = (DATA.menu && Array.isArray(DATA.menu.items)) ? DATA.menu.items : [];

  // -----------------------------------------------------------------------
  // #es-hero
  // -----------------------------------------------------------------------
  function renderHero() {
    const root = mount("es-hero");
    if (!root) return;
    const inner = el("div", { class: "es-hero__inner" });

    inner.appendChild(el("p", { class: "es-hero__eyebrow", text: "Secrets Posture Assessment" }));
    inner.appendChild(el("h1", { class: "es-hero__title", text: "Executive Summary" }));

    const dl = el("dl", { class: "es-hero__meta" });
    const addMeta = (label, value) => {
      dl.appendChild(el("dt", { class: "es-hero__meta-label", text: label }));
      dl.appendChild(el("dd", { class: "es-hero__meta-value", text: value }));
    };
    if (meta.client) addMeta("Client", meta.client);
    if (meta.as_of) addMeta("As of", meta.as_of);
    if (meta.total_ucs != null) addMeta("Use cases assessed", meta.total_ucs);
    if (dl.childNodes.length) inner.appendChild(dl);

    const scope = Array.isArray(meta.frameworks_scope) ? meta.frameworks_scope : [];
    if (scope.length) {
      const wrap = el("div", { class: "es-hero__scope", attrs: { "aria-label": "Frameworks in scope" } });
      wrap.appendChild(el("span", { class: "es-hero__scope-label", text: "Frameworks in scope" }));
      const list = el("ul", { class: "es-chip-row" });
      for (const fw of scope) {
        list.appendChild(el("li", { children: [chip(fw, "es-chip--framework")] }));
      }
      wrap.appendChild(list);
      inner.appendChild(wrap);
    }
    root.appendChild(inner);
  }

  // -----------------------------------------------------------------------
  // #es-snapshot — animated count-up tiles
  // -----------------------------------------------------------------------
  // Count-up flourish. The node already carries its true final (textContent +
  // dataset.value) BEFORE this runs, so any static capture is correct even if
  // the animation never starts. We only ever animate 0 -> target and always
  // settle exactly on target.
  function animateCount(node, target) {
    if (reduceMotion || target <= 0) {
      // Leave the final value already painted by renderSnapshot.
      return;
    }
    const duration = 900;
    const start = performance.now();
    function frame(now) {
      const t = Math.min(1, (now - start) / duration);
      const eased = 1 - Math.pow(1 - t, 3); // easeOutCubic
      if (t < 1) {
        node.textContent = String(Math.round(eased * target));
        requestAnimationFrame(frame);
      } else {
        node.textContent = node.dataset.value; // guaranteed exact final
      }
    }
    node.textContent = "0";
    requestAnimationFrame(frame);
  }

  function renderSnapshot() {
    const root = mount("es-snapshot");
    if (!root) return;
    root.appendChild(el("h2", { class: "es-section__title", text: "Posture snapshot" }));
    const grid = el("div", { class: "es-snapshot__grid" });
    for (const s of SNAPSHOT_STATES) {
      const value = Number(snapshot[s.key] || 0);
      const tile = el("div", {
        class: `es-tile ${s.cls}`,
        attrs: { "data-state": s.key },
      });
      // Set the TRUE final value immediately: as textContent (so the very first
      // paint is correct) and as data-value (the source of truth for print and
      // animation end). Any print/PDF/screenshot is correct regardless of when
      // it is taken.
      const num = el("span", {
        class: "es-tile__count",
        text: value,
        attrs: { "aria-hidden": "false", "data-value": String(value) },
      });
      tile.appendChild(num);
      tile.appendChild(el("span", { class: "es-tile__label", text: s.label }));
      grid.appendChild(tile);
      animateCount(num, value);
    }
    root.appendChild(grid);

    // Print safety: force every counter to its true final before any print so
    // Print -> Save as PDF never captures a mid-animation value. Belt and
    // braces: both the beforeprint event and a print media-query listener.
    const forceFinals = () => {
      for (const num of root.querySelectorAll(".es-tile__count")) {
        if (num.dataset.value != null) num.textContent = num.dataset.value;
      }
    };
    window.addEventListener("beforeprint", forceFinals);
    if (typeof window.matchMedia === "function") {
      const mql = window.matchMedia("print");
      const onPrint = (e) => { if (e.matches) forceFinals(); };
      if (typeof mql.addEventListener === "function") mql.addEventListener("change", onPrint);
      else if (typeof mql.addListener === "function") mql.addListener(onPrint);
    }
  }

  // -----------------------------------------------------------------------
  // Engagement card (shared by tier + board)
  // -----------------------------------------------------------------------
  let cardSeq = 0;
  function engagementCard(item, opts) {
    const expanded = !!(opts && opts.expanded);
    const card = el("article", {
      class: "es-card " + (STATE_CLASS[item.state] || ""),
      attrs: { "data-quadrant": item.quadrant || "", "data-state": item.state || "" },
    });

    const head = el("header", { class: "es-card__head" });
    head.appendChild(el("span", { class: "es-card__uc", text: item.uc_id }));
    head.appendChild(chip(item.state, "es-chip--state " + (STATE_CLASS[item.state] || "")));
    card.appendChild(head);

    const meta2 = el("div", { class: "es-card__meta" });
    if (item.risk_band) meta2.appendChild(chip("Risk · " + item.risk_band, "es-chip--risk"));
    if (item.effort_band) meta2.appendChild(chip("Effort · " + item.effort_band, "es-chip--effort"));
    const d0 = firstDriver(item);
    if (d0) {
      const dchip = chip(driverLabel(d0), "es-chip--driver");
      if (d0.control_short_title) dchip.setAttribute("title", d0.control_short_title);
      meta2.appendChild(dchip);
    }
    if (meta2.childNodes.length) card.appendChild(meta2);

    if (item.proposed_engagement) {
      card.appendChild(el("p", { class: "es-card__engagement", text: item.proposed_engagement }));
    }

    // Expandable detail: dependency + full driver list.
    const drivers = Array.isArray(item.regulatory_driver) ? item.regulatory_driver : [];
    const hasDetail = !!item.dependency || drivers.length > 0;
    if (hasDetail && !expanded) {
      const panelId = `es-detail-${++cardSeq}`;
      const btn = el("button", {
        class: "es-card__toggle",
        text: "Details",
        attrs: { type: "button", "aria-expanded": "false", "aria-controls": panelId },
      });
      const panel = buildDetail(drivers, item.dependency);
      panel.id = panelId;
      panel.hidden = true;
      btn.addEventListener("click", () => {
        const open = btn.getAttribute("aria-expanded") === "true";
        btn.setAttribute("aria-expanded", open ? "false" : "true");
        panel.hidden = open;
      });
      card.appendChild(btn);
      card.appendChild(panel);
    } else if (hasDetail && expanded) {
      card.appendChild(buildDetail(drivers, item.dependency));
    }
    return card;
  }

  function buildDetail(drivers, dependency) {
    const panel = el("div", { class: "es-card__detail" });
    if (dependency) {
      const dep = el("div", { class: "es-card__dependency" });
      dep.appendChild(el("span", { class: "es-card__detail-label", text: "Dependency" }));
      dep.appendChild(el("p", { class: "es-card__detail-text", text: dependency }));
      panel.appendChild(dep);
    }
    if (drivers.length) {
      const wrap = el("div", { class: "es-card__drivers" });
      wrap.appendChild(el("span", { class: "es-card__detail-label", text: "Regulatory drivers" }));
      const list = el("ul", { class: "es-driver-list" });
      for (const d of drivers) {
        const li = el("li", { class: "es-driver" });
        li.appendChild(el("span", { class: "es-driver__code", text: driverLabel(d) }));
        if (d.control_short_title) {
          li.appendChild(el("span", { class: "es-driver__title", text: d.control_short_title }));
        }
        list.appendChild(li);
      }
      wrap.appendChild(list);
      panel.appendChild(wrap);
    }
    return panel;
  }

  // -----------------------------------------------------------------------
  // #es-tier — prioritised cards (Quick wins, then Major projects)
  // -----------------------------------------------------------------------
  function renderTier() {
    const root = mount("es-tier");
    if (!root) return;
    root.appendChild(el("h2", { class: "es-section__title", text: "Prioritised engagement tier" }));
    for (const q of TIER_QUADRANTS) {
      const tierItems = filterItems(items, { quadrant: q });
      if (!tierItems.length) continue;
      const block = el("div", { class: "es-tier__block", attrs: { "data-quadrant": q } });
      const header = el("div", { class: "es-tier__header" });
      header.appendChild(el("h3", { class: "es-tier__heading", text: q }));
      header.appendChild(el("span", { class: "es-tier__count", text: `${tierItems.length}` }));
      block.appendChild(header);
      const grid = el("div", { class: "es-card-grid" });
      for (const it of tierItems) grid.appendChild(engagementCard(it, { expanded: false }));
      block.appendChild(grid);
      root.appendChild(block);
    }
  }

  // -----------------------------------------------------------------------
  // #es-board — full grid with filter + sort controls
  // -----------------------------------------------------------------------
  function renderBoard() {
    const root = mount("es-board");
    if (!root) return;
    root.appendChild(el("h2", { class: "es-section__title", text: "Engagement board" }));

    const present = (field, order) =>
      order.filter(v => items.some(it => it[field] === v));
    const quadOptions = present("quadrant", QUADRANTS);
    const stateOptions = present("state", ["MET", "PARTIAL", "GAP", "PENDING"]);

    const ctrl = { quadrant: "", state: "", sort: "risk" };

    const controls = el("form", {
      class: "es-board__controls",
      attrs: { "aria-label": "Board filters" },
    });
    controls.addEventListener("submit", (e) => e.preventDefault());

    const buildSelect = (id, label, options, onChange) => {
      const field = el("div", { class: "es-field" });
      field.appendChild(el("label", { class: "es-field__label", text: label, attrs: { for: id } }));
      const sel = el("select", { class: "es-field__select", attrs: { id } });
      sel.appendChild(el("option", { text: "All", attrs: { value: "" } }));
      for (const o of options) sel.appendChild(el("option", { text: o, attrs: { value: o } }));
      sel.addEventListener("change", () => onChange(sel.value));
      field.appendChild(sel);
      return field;
    };

    controls.appendChild(buildSelect("es-filter-quadrant", "Quadrant", quadOptions, (v) => {
      ctrl.quadrant = v; paint();
    }));
    controls.appendChild(buildSelect("es-filter-state", "State", stateOptions, (v) => {
      ctrl.state = v; paint();
    }));

    // Sort toggle (risk <-> effort).
    const sortField = el("div", { class: "es-field" });
    sortField.appendChild(el("span", { class: "es-field__label", text: "Sort by" }));
    const sortBtn = el("button", {
      class: "es-sort-toggle",
      attrs: { type: "button", "aria-pressed": "false", "data-sort": "risk" },
    });
    const updateSortLabel = () => {
      sortBtn.textContent = ctrl.sort === "risk" ? "Risk" : "Effort";
      sortBtn.setAttribute("data-sort", ctrl.sort);
      sortBtn.setAttribute("aria-pressed", ctrl.sort === "effort" ? "true" : "false");
    };
    sortBtn.addEventListener("click", () => {
      ctrl.sort = ctrl.sort === "risk" ? "effort" : "risk";
      updateSortLabel(); paint();
    });
    updateSortLabel();
    sortField.appendChild(sortBtn);
    controls.appendChild(sortField);

    root.appendChild(controls);

    const status = el("p", { class: "es-board__status", attrs: { "aria-live": "polite" } });
    root.appendChild(status);

    const grid = el("div", { class: "es-card-grid es-board__grid" });
    root.appendChild(grid);

    function paint() {
      const filtered = sortItems(
        filterItems(items, { quadrant: ctrl.quadrant || null, state: ctrl.state || null }),
        ctrl.sort);
      grid.textContent = "";
      status.textContent = `${filtered.length} of ${items.length} engagements`;
      if (!filtered.length) {
        grid.appendChild(el("p", { class: "es-board__empty", text: "No engagements match these filters." }));
        return;
      }
      for (const it of filtered) grid.appendChild(engagementCard(it, { expanded: false }));
    }
    paint();
  }

  // -----------------------------------------------------------------------
  // #es-appendix — grouped, fully-expanded (print-primary)
  // -----------------------------------------------------------------------
  function renderAppendix() {
    const root = mount("es-appendix");
    if (!root) return;
    root.appendChild(el("h2", { class: "es-section__title", text: "Full engagement menu" }));
    const groups = groupByQuadrant(items);
    for (const q of QUADRANTS) {
      const list = groups[q] || [];
      if (!list.length) continue;
      const block = el("section", { class: "es-appendix__group", attrs: { "data-quadrant": q } });
      const header = el("div", { class: "es-appendix__header" });
      header.appendChild(el("h3", { class: "es-appendix__heading", text: q }));
      header.appendChild(el("span", { class: "es-appendix__count", text: `${list.length}` }));
      block.appendChild(header);
      const grid = el("div", { class: "es-card-grid es-appendix__grid" });
      for (const it of list) grid.appendChild(engagementCard(it, { expanded: true }));
      block.appendChild(grid);
      root.appendChild(block);
    }
  }

  function boot() {
    renderHero();
    renderSnapshot();
    renderTier();
    renderBoard();
    renderAppendix();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
}

if (typeof module !== "undefined" && module.exports)
  module.exports = { groupByQuadrant, sortItems, filterItems };
