type Option = { value: string; label: string };

export function ToggleGroup(
  { value, onChange, options }:
  { value: string | null; onChange: (v: string | null) => void; options: Option[] },
) {
  return (
    <div className="inline-flex rounded-sm border border-border-strong overflow-hidden bg-bg2 p-[3px] gap-[3px]">
      {options.map(o => {
        const on = value === o.value;
        return (
          <button key={o.value} type="button" aria-pressed={on}
            onClick={() => onChange(on ? null : o.value)}
            className={`h-8 px-4 rounded-xs text-[12.5px] font-medium font-body transition-colors ${
              on ? 'bg-card text-ink shadow-sm' : 'text-muted hover:text-ink2'}`}>
            {o.label}
          </button>
        );
      })}
    </div>
  );
}
