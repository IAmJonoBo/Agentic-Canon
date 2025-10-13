import { expect, test } from '@playwright/test';

test('home page loads', async ({ page }) => {
  await page.goto('/');

  // Check that the page loaded
  await expect(page.locator('h1')).toBeVisible();

  // Check for the project name
  await expect(page.locator('h1')).toContainText('{{cookiecutter.project_name}}');
});

test('page has description', async ({ page }) => {
  await page.goto('/');

  // Check for the description
  await expect(page.getByText('{{cookiecutter.description}}')).toBeVisible();
});
