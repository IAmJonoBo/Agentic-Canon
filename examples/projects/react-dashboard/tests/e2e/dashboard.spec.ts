import { test, expect } from '@playwright/test';

test.describe('React dashboard example', () => {
  test('shows dashboard metrics and navigates between pages', async ({ page }) => {
    await page.goto('/');

    await expect(page.getByRole('heading', { name: 'Engineering operations' })).toBeVisible();

    await page.getByRole('button', { name: /Deployments/i }).click();

    await page.getByRole('link', { name: 'Analytics' }).click();
    await expect(page.getByRole('heading', { name: 'Predictive analytics' })).toBeVisible();

    await page.getByRole('link', { name: 'Reports' }).click();
    await expect(page.getByRole('cell', { name: 'Checkout' })).toBeVisible();
  });
});
