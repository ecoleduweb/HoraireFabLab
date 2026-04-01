import { test, expect } from '@playwright/test';
import { ApiMocker } from '../Helper/mockApi.ts';
import { loginMocks } from "../Helper/Mocks/login.mock.ts";

test.describe('authentication', () => {

    test.beforeEach(async ({ page }) => {
        await page.clock.install({ time: new Date('2025-03-22T08:00:00') });
        await page.goto('http://localhost:5002/login');
        await page.waitForLoadState('networkidle');
    });
    
    test('LoginSucessfull', async ({ page }) => {
        const apiMocker = new ApiMocker(page);
        await apiMocker.addMocks([
            //  loginMocks.notFound,
            loginMocks.success
        ])
        .apply();
        await page.locator('#username').fill('playwright');
        await page.locator('#password').fill('pw123');
        await page.getByText('Se connecter').click();
        expect(page.url()).toBe('https://localhost:5002/admin');
    });
});