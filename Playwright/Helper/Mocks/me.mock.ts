import type { MockConfig } from "../types.ts";

export const meMocks = {
    success: {
        method: 'GET',
        url: '/user/me',
        response: {
            status: 200,
            json: {
                username: 'playwright'
            }
        }
    }
} satisfies Record<string, MockConfig>;