import { test as base, expect } from '@playwright/test';


const FIXED_LOCAL_ISO = new Date('2024-02-25T12:00:00-05:00');
export const test = base.extend({
  page: async ({ page }, use) => {
    await page.clock.install({ time: FIXED_LOCAL_ISO });
    await use(page);
  },
});

export { expect };
