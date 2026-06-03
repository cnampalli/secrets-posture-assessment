import { type InputHTMLAttributes } from 'react';
export function Checkbox(props: InputHTMLAttributes<HTMLInputElement>) {
  return <input type="checkbox" className="w-[17px] h-[17px] mt-0.5 accent-accent cursor-pointer shrink-0" {...props} />;
}
