import { POST } from '../ts/server.ts';
import type { CreateEventPayload, Event } from '../modelse/Event.ts';

export const EventService = {
    async createEvent(name: string, eventDate: string): Promise<void> {
        await POST<CreateEventPayload, Event>('/events', { name, eventDate });
    }
};