import type { MockConfig } from "../types.ts";

export const loginMocks = {
    success: {
        method: 'POST',
        url: '/login',
        response: {
            status: 200,
            json:{}
        }
    }
} satisfies Record<string, MockConfig>;