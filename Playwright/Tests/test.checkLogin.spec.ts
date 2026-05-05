import { test, expect } from "@playwright/test";
import { ApiMocker } from "../Helper/mockApi.ts";
import { loginMocks } from "../Helper/Mocks/login.mock.ts";
import { meMocks } from "../Helper/Mocks/me.mock.ts";

test.describe("authentication", () => {
  test.beforeEach(async ({ page }) => {
    await page.clock.install({ time: new Date("2025-03-22T08:00:00") });

    const apiMocker = new ApiMocker(page);
    await apiMocker.addMocks([loginMocks.success, meMocks.success]).apply();

    await page.goto("/login");
    await page.waitForLoadState("networkidle");
  });

  test("LoginSuccessful", async ({ page }) => {
    const apiMocker = new ApiMocker(page);
    await page.locator("#username").fill("playwright");
    await page.locator("#password").fill("pw123");
    await page.getByText("Se connecter").click();
    await expect(page).toHaveURL("http://localhost:5002/admin");
  });
});
