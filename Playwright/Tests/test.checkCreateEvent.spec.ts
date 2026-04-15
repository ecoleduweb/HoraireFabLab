import { test, expect } from '@playwright/test';
import { ApiMocker } from '../Helper/mockApi.ts';
import { eventMocks } from "../Helper/Mocks/event.mock.ts";
import { meMocks } from "../Helper/Mocks/me.mock.ts";

test.describe('events', () => {

    test.beforeEach(async ({ page }) => {
        await page.clock.install({ time: new Date('2025-03-22T08:00:00') });

        const apiMocker = new ApiMocker(page);
        await apiMocker.addMocks([
            meMocks.success
        ]).apply();

        await page.goto('/admin/events/create');
        await page.waitForLoadState('networkidle');
    });

    test('CreateEventSuccessful', async ({ page }) => {
        const apiMocker = new ApiMocker(page);
        await apiMocker.addMocks([
            eventMocks.createSuccess
        ]).apply();

        await page.locator('#name').fill('Journée portes ouvertes FabLab');
        await page.locator('#event_date').fill('2025-04-15');
        await page.getByText("Créer l'événement").click();

        await page.waitForURL('**/admin');
        await expect(page).toHaveURL('http://localhost:5002/admin');
    });

    test('CreateEventButtonDisabledWhenEmpty', async ({ page }) => {
        const button = page.locator('button[type="submit"]');
        await expect(button).toBeDisabled();
    });

    test('CreateEventServerError', async ({ page }) => {
        const apiMocker = new ApiMocker(page);
        await apiMocker.addMocks([
            eventMocks.createError
        ]).apply();

        await page.locator('#name').fill('Événement test');
        await page.locator('#event_date').fill('2025-04-15');
        await page.getByText("Créer l'événement").click();

        await expect(page.locator('.error-banner')).toBeVisible();
    });
});