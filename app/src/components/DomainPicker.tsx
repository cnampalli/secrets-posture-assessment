import { useAssessment } from '../assessment/store';
import { DOMAINS, type DomainId } from '../assessment/domains';

export function DomainPicker() {
  const a = useAssessment();
  return (
    <label className="flex items-center gap-1.5 text-sm">
      <span className="sr-only">Assessment domain</span>
      <select
        aria-label="Assessment domain"
        value={a.domainId}
        onChange={e => a.setDomain(e.target.value as DomainId)}
        className="bg-bg2 border border-border rounded-sm px-2 py-1 text-ink2 font-display"
      >
        {DOMAINS.map(d => <option key={d.id} value={d.id}>{d.label}</option>)}
      </select>
    </label>
  );
}
