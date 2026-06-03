import { createContext, useContext, useState, useCallback, type ReactNode } from 'react';
const Ctx = createContext<(m: string) => void>(() => {});
export function ToastProvider({ children }: { children: ReactNode }) {
  const [msg, setMsg] = useState<string | null>(null);
  const toast = useCallback((m: string) => { setMsg(m); setTimeout(() => setMsg(null), 1800); }, []);
  return (
    <Ctx.Provider value={toast}>
      {children}
      {msg && <div role="status" className="fixed bottom-6 left-1/2 -translate-x-1/2 bg-ink text-bg px-4 py-2.5 rounded-sm text-sm shadow-lg z-50">{msg}</div>}
    </Ctx.Provider>
  );
}
export const useToast = () => useContext(Ctx);
