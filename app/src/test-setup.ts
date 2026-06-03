import '@testing-library/jest-dom';

// Node v26 exposes localStorage/sessionStorage as experimental globals but they
// are undefined (not initialised without --localstorage-file). Vitest's jsdom
// environment populates globalThis from the jsdom window, but skips any key that
// already exists on globalThis unless it is listed in the hard-coded KEYS array.
// Since localStorage/sessionStorage are not in that list, they stay as the Node
// v26 undefined stubs instead of the jsdom Storage implementations.
// Fix: read the real Storage objects from the underlying jsdom instance that
// vitest attaches to globalThis.jsdom, then patch globalThis explicitly.
// @ts-expect-error – vitest attaches the jsdom instance as globalThis.jsdom
const _jsdomWindow = typeof globalThis.jsdom !== 'undefined' ? globalThis.jsdom.window : undefined;
if (_jsdomWindow) {
  Object.defineProperty(globalThis, 'localStorage', {
    value: _jsdomWindow.localStorage,
    writable: true,
    configurable: true,
  });
  Object.defineProperty(globalThis, 'sessionStorage', {
    value: _jsdomWindow.sessionStorage,
    writable: true,
    configurable: true,
  });
}
