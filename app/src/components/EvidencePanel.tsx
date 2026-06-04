import { useRef, useState } from 'react';
import { useAssessment } from '../assessment/store';
import { useToast } from './Toast';
import { humanSize } from '../assessment/evidence';

export function EvidencePanel() {
  const a = useAssessment();
  const toast = useToast();
  const uc = a.current;
  const files = a.evidenceFor(uc.uc_id);
  const inputRef = useRef<HTMLInputElement>(null);
  const [drag, setDrag] = useState(false);

  async function add(list: FileList | File[]) {
    const { rejected } = await a.addEvidence(list);
    if (rejected.length) toast(rejected[0]);
  }

  return (
    <section className="mt-6">
      <div className="flex items-center gap-2 mb-2">
        <span className="font-mono text-[10px] tracking-widest uppercase text-muted">Evidence</span>
        {files.length > 0 && <span className="font-mono text-[10px] text-faint">{files.length} file{files.length > 1 ? 's' : ''}</span>}
      </div>
      <div
        role="button" tabIndex={0} aria-label="Attach evidence files"
        onClick={() => inputRef.current?.click()}
        onKeyDown={e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); inputRef.current?.click(); } }}
        onDragOver={e => { e.preventDefault(); setDrag(true); }}
        onDragLeave={() => setDrag(false)}
        onDrop={e => { e.preventDefault(); setDrag(false); if (e.dataTransfer.files.length) void add(e.dataTransfer.files); }}
        className={`cursor-pointer rounded-md border border-dashed px-4 py-5 text-center text-sm transition-colors focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent ${
          drag ? 'border-accent bg-accent-soft text-ink' : 'border-border-strong bg-bg2 text-muted hover:border-accent'}`}
      >
        <div className="font-medium">⬆ Drag files here or click to browse</div>
        <div className="text-xs text-faint mt-1">PDF · images · Office docs — max 10 MB each</div>
      </div>
      <input
        ref={inputRef} data-testid="evidence-input" type="file" multiple className="hidden"
        accept=".pdf,.png,.jpg,.jpeg,.webp,.txt,.csv,.docx,.xlsx,.pptx"
        onChange={e => { const fl = e.target.files; if (fl && fl.length) void add(fl); e.currentTarget.value = ''; }}
      />
      {files.length > 0 && (
        <ul className="flex flex-wrap gap-2 mt-3">
          {files.map(f => (
            <li key={f.id} className="inline-flex items-center gap-2 bg-card border border-border rounded-pill pl-3 pr-2 py-1 text-[12.5px]">
              <span className="truncate max-w-[200px]">{f.name}</span>
              <span className="font-mono text-[10.5px] text-faint">{humanSize(f.size)}</span>
              <button type="button" aria-label={`Remove ${f.name}`} onClick={() => void a.removeEvidence(f.id)}
                className="text-muted hover:text-gap leading-none px-1">✕</button>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
