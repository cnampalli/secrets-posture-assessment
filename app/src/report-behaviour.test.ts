// H5 — report SPA behavioural tests.
//
// The byte-snapshot (tests/test_report_render.py) proves the report renders
// DETERMINISTICALLY; these prove it BEHAVES. We load the real rendered report
// (matrix/domains/secrets/secrets-report.html) into a jsdom window with its
// scripts running — i.e. the actual shipped single-file SPA — and exercise the
// four interactive behaviours the plan calls out: posture-count math, gap-link
// navigation, compliance-cascade filtering, and MET-override persistence.
import { describe, it, expect } from 'vitest';
import { JSDOM, VirtualConsole } from 'jsdom';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

// vitest runs from app/ (CI: `cd app && npm run test`); the report lives at repo/matrix/.
const REPORT = resolve(process.cwd(), '..', 'matrix', 'domains', 'secrets', 'secrets-report.html');
const HTML = readFileSync(REPORT, 'utf8');

// Boot the report's real SPA in a fresh jsdom window (scripts run on construction;
// renderDashboard()/renderTable()/the cascade IIFE all execute synchronously).
function bootReport(): any {
  const virtualConsole = new VirtualConsole(); // swallow the report's console output
  const dom = new JSDOM(HTML, {
    runScripts: 'dangerously',
    pretendToBeVisual: true,
    url: 'https://report.test/',
    virtualConsole,
  });
  return dom.window as any;
}

// non-placeholder <li> count for a dashboard list
function realItems(w: any, id: string): number {
  return Array.from(w.document.getElementById(id).querySelectorAll('li')).filter(
    (li: any) => !li.classList.contains('muted'),
  ).length;
}

describe('report SPA behaviour (H5)', () => {
  it('boots: the dashboard renders posture + lists', () => {
    const w = bootReport();
    expect(w.document.getElementById('posture-legend')!.textContent).toMatch(/MET|GAP/);
    expect(typeof w.goToUC).toBe('function');
    expect(typeof w.toggleMet).toBe('function');
  });

  it('posture-count math: legend counts equal the detailed-list lengths', () => {
    const w = bootReport();
    const legend = w.document.getElementById('posture-legend')!;
    const counts: Record<string, number> = {};
    legend.querySelectorAll('.pill').forEach((p: any) => {
      const b = p.nextElementSibling;
      if (b && b.tagName === 'B') counts[p.textContent.trim()] = Number(b.textContent);
    });
    // the math behind the bar must agree with what the GAP/PARTIAL/PENDING lists show
    expect(counts.GAP).toBe(realItems(w, 'gaplist'));
    expect(counts.PARTIAL).toBe(realItems(w, 'partiallist'));
    expect(counts.PENDING).toBe(realItems(w, 'pendinglist'));
    const total = counts.MET + counts.PARTIAL + counts.GAP + counts.PENDING;
    expect(total).toBeGreaterThan(0);
  });

  it('gap-link navigation: clicking a gap item opens that use case', () => {
    const w = bootReport();
    const gapLi = w.document.querySelector('#gaplist li:not(.muted)') as any;
    expect(gapLi).toBeTruthy();
    const ucId = gapLi.querySelector('.id').textContent.trim();
    gapLi.click(); // inline onclick="goToUC('...')" executes in jsdom
    expect((w.document.getElementById('uc-select') as any).value).toBe(ucId);
    expect(w.document.getElementById('view-uc').classList.contains('active')).toBe(true);
    expect(w.document.getElementById('uc-card').textContent).toContain(ucId);
  });

  it('MET-override persistence: toggleMet writes localStorage and adjusts posture; loadOv reads it back', () => {
    const w = bootReport();
    const gapLi = w.document.querySelector('#gaplist li:not(.muted)') as any;
    const ucId = gapLi.querySelector('.id').textContent.trim();

    w.toggleMet(ucId);
    const stored = JSON.parse(w.localStorage.getItem('fi_overrides') || '{}');
    expect(stored[ucId]).toBe(true); // persisted to storage
    expect(w.loadOv()[ucId]).toBe(true); // read back
    expect(w.effState({ uc_id: ucId, current_state: 'GAP' })).toBe('MET'); // applied
    expect(w.document.getElementById('posture-adj')!.textContent).toContain('marked MET');

    w.toggleMet(ucId); // toggling off clears it
    expect(JSON.parse(w.localStorage.getItem('fi_overrides') || '{}')[ucId]).toBeUndefined();
  });

  it('compliance cascade: clicking a framework populates its controls', () => {
    const w = bootReport();
    const fwItem = w.document.querySelector('#casc-fw .item') as any;
    expect(fwItem).toBeTruthy(); // frameworks rendered on boot
    fwItem.click();
    expect(w.document.querySelectorAll('#casc-ctrl .item').length).toBeGreaterThan(0);
  });
});
