import { GET, POST } from '../ts/server.ts';
import type {EventForm, RepairEvent} from '../models/RepairEvent.ts';


export const EventService = {
    async createEvent(name: string, eventDate: string): Promise<void> {
        await POST<EventForm, RepairEvent>('/events', { name, eventDate });
    }
};


// Retourne le premier événement actif.
export async function fetchActiveEvent(): Promise<RepairEvent> {
    const events = await GET<RepairEvent[]>("/events/active", false)
    return events[0]
}