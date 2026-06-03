import { type ButtonHTMLAttributes } from 'react';

type Variant = 'primary' | 'outline' | 'ghost';
const base = 'inline-flex items-center gap-2 rounded-sm font-body font-semibold text-sm h-9 px-4 cursor-pointer transition-colors disabled:opacity-40 disabled:cursor-not-allowed';
const variants: Record<Variant, string> = {
  primary: 'bg-accent text-accent-fg hover:brightness-95',
  outline: 'bg-card text-ink border border-border hover:bg-bg2',
  ghost: 'bg-transparent text-ink hover:bg-bg2',
};

export function Button(
  { variant = 'primary', className = '', ...props }:
  ButtonHTMLAttributes<HTMLButtonElement> & { variant?: Variant },
) {
  return <button className={`${base} ${variants[variant]} ${className}`} {...props} />;
}
