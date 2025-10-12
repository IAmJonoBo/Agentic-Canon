import { useCallback } from 'react';
import { create } from 'zustand';
import type { AuthState } from '../types/auth';
import { authenticate } from '../services/api';

type AuthStore = AuthState & {
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
};

const useAuthStore = create<AuthStore>((set) => ({
  token: null,
  user: null,
  login: async (email: string, password: string) => {
    const token = await authenticate(email, password);
    set({
      token,
      user: {
        email,
        name: email.split('@')[0].replace('.', ' '),
        role: email.startsWith('sre') ? 'SRE' : 'Engineer',
      },
    });
  },
  logout: () => set({ token: null, user: null }),
}));

export function useAuth() {
  const token = useAuthStore((state) => state.token);
  const user = useAuthStore((state) => state.user);
  const login = useAuthStore((state) => state.login);
  const logout = useAuthStore((state) => state.logout);

  const isAuthenticated = Boolean(token);

  const handleLogout = useCallback(() => {
    logout();
  }, [logout]);

  return { token, user, login, logout: handleLogout, isAuthenticated };
}
