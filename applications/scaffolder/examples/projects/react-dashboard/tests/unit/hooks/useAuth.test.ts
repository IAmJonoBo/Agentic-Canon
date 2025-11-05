import { act, renderHook, waitFor } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { useAuth } from '../../../src/hooks/useAuth';

const VALID_EMAIL = 'engineer@example.com';
const PASSWORD = 'correct horse battery staple';

describe('useAuth', () => {
  it('logs in with example.com domain', async () => {
    const { result } = renderHook(() => useAuth());

    await act(async () => {
      await result.current.login(VALID_EMAIL, PASSWORD);
    });

    await waitFor(() => expect(result.current.isAuthenticated).toBe(true));
    expect(result.current.user?.email).toBe(VALID_EMAIL);
  });

  it('fails with non-company email', async () => {
    const { result } = renderHook(() => useAuth());

    await expect(result.current.login('user@other.com', PASSWORD)).rejects.toThrow(
      'Invalid corporate email',
    );
  });
});
