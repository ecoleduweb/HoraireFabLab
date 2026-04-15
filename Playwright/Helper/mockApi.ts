import { Page } from "@playwright/test";
import type { MockConfig } from "./types.ts";

export class ApiMocker {
  private page: Page;
  private mockConfigs: MockConfig[] = [];

  constructor(page: Page) {
    this.page = page;
  }

  // Chainable method to add a single mock configuration
  addMock(config: MockConfig): this {
    this.mockConfigs.push(config);
    return this;
  }

  // Chainable method to add multiple mock configurations
  addMocks(configs: MockConfig[]): this {
    this.mockConfigs.push(...configs);
    return this;
  }

  // Method to apply all collected mock configurations
  async apply(): Promise<void> {
    for (const config of this.mockConfigs) {
      await this.page.route(`**${config.url}`, async (route) => {
        if (route.request().method() === config.method) {
          await route.fulfill({
            status: config.response.status,
            json: config.response.json,
            headers: config.response.headers,
          });
        } else {
          await route.continue();
        }
      });
    }
    this.mockConfigs = [];
  }

  // Optional method to clear all mock routes
  async clearMocks(): Promise<void> {
    await this.page.unroute("**");
    this.mockConfigs = [];
  }
}