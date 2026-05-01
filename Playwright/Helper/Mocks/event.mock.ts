import type { MockConfig } from "../types.ts";

export const eventMocks = {
    createSuccess: {
        method: 'POST',
        url: '/events',
        response: {
            status: 201,
            json: {
                id: 1,
                name: 'Journée portes ouvertes FabLab',
                eventDate: '2025-04-15'
            }
        }
    },
    createError: {
        method: 'POST',
        url: '/events',
        response: {
            status: 400,
            json: {
                detail: 'Une erreur est survenue'
            }
        }
    },
    updateSuccess: {
        method: 'PUT',
        url: '/events/1/update_date',
        response: {
            status: 200,
            json: {
                id: 1,
                name: 'Journée portes ouvertes FabLab',
                eventDate: '2025-04-15'
            }
        }
    },
    updateError: {
        method: 'PUT',
        url: '/events/1/update_date',
        response: {
            status: 400,
            json: {
                detail: 'Une erreur est survenue'
            }
        }
    }
} satisfies Record<string, MockConfig>;