import { type ReactNode } from 'react';

type State = 'met' | 'partial' | 'gap' | 'pending' | 'na';
const stateCls: Record<State, string> = {
  met: 'text-met bg-met-soft', partial: 'text-partial bg-partial-soft',
  gap: 'text-gap bg-gap-soft', pending: 'text-pending bg-pending-soft', na: 'text-na bg-na-soft',
};

export function Badge(
  { state, outline, className = '', children }:
  { state?: State; outline?: boolean; className?: string; children: ReactNode },
) {
  const tone = state ? stateCls[state] : outline ? 'text-muted bg-card border border-border' : 'text-muted bg-bg2';
  return (
    <span className={`inline-flex items-center gap-1.5 h-[22px] px-2.5 rounded-pill font-mono text-[11.5px] font-medium ${tone} ${className}`}>
      {state && <span className="w-1.5 h-1.5 rounded-full bg-current opacity-80" />}
      {children}
    </span>
  );
}
