export interface AuthState {
  token: string | null;
  user: {
    name: string;
    email: string;
    role: string;
  } | null;
}
