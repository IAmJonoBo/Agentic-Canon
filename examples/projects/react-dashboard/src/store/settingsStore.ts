import { create } from 'zustand';

interface SettingsState {
  theme: 'light' | 'dark';
  enableRealtime: boolean;
  toggleTheme: () => void;
  toggleRealtime: () => void;
}

export const useSettingsStore = create<SettingsState>((set, get) => ({
  theme: 'light',
  enableRealtime: true,
  toggleTheme: () => {
    const next = get().theme === 'light' ? 'dark' : 'light';
    const root = window.document.documentElement;
    root.classList.remove('light', 'dark');
    root.classList.add(next);
    set({ theme: next });
  },
  toggleRealtime: () => set(({ enableRealtime }) => ({ enableRealtime: !enableRealtime })),
}));
