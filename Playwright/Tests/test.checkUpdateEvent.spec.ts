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
        await page.goto('/admin/events/modify?id=1');
        await page.waitForLoadState('networkidle');
    });

    test('UpdateEventSuccessful', async ({ page }) => {
        const apiMocker = new ApiMocker(page);
        await apiMocker.addMocks([
            eventMocks.updateSuccess
        ]).apply();
        await page.locator('#name').fill('Journée portes ouvertes FabLab');
        await page.locator('#event_date').fill('2025-04-15');
        await page.getByText("Modifier l'événement").click();
        await page.waitForURL('**/admin');
        await expect(page).toHaveURL('http://localhost:5002/admin');
    });

    test('UpdateEventServerError', async ({ page }) => {
        const apiMocker = new ApiMocker(page);
        await apiMocker.addMocks([
            eventMocks.updateError
        ]).apply();
        await page.locator('#name').fill('Journée portes ouvertes FabLab');
        await page.locator('#event_date').fill('2025-04-15');
        const dialogPromise = page.waitForEvent('dialog');
        await page.getByText("Modifier l'événement").click();
        const dialog = await dialogPromise;
        await expect(dialog.message()).toBe('Une erreur est survenue');
        await dialog.accept();
        await expect(page).toHaveURL('http://localhost:5002/admin/events/modify?id=1');
    });
});