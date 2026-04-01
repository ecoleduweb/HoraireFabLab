import type { MockConfig } from "../types.ts";

export const loginMocks = {
    notFound: {
        url: '/login',
        response: {
            status: 404,
            json: { message: "User not found" }
        }
    },
    success: {
        method: 'POST',
        url: '/login',
        response: {
            status: 200,
            json:{}
        }
    }
} satisfies Record<string, MockConfig>;