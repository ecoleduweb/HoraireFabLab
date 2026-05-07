import { GET, POST, PUT } from '../ts/server.ts';
import type { EventForm, RepairEvent, UpdateRepairEvent } from '../models/RepairEvent.ts';

export const EventService = {
	async createEvent(name: string, eventDate: string): Promise<void> {
		await POST<EventForm, RepairEvent>('/events', { name, eventDate });
	},

	async getEvents(): Promise<RepairEvent[]> {
		return await GET<RepairEvent[]>('/events/all_events');
	},
	async updateEvent(eventId: number, name: string, eventDate: string): Promise<void> {
		await PUT<UpdateRepairEvent, RepairEvent>(`/events/${eventId}/update_date`, {
			id: eventId,
			name,
			eventDate
		});
	},
	async getEventById(eventId: number): Promise<RepairEvent> {
		return await GET<RepairEvent>(`/events/${eventId}`);
	}
};

// Retourne le premier événement actif.
export async function fetchActiveEvent(): Promise<RepairEvent> {
	const events = await GET<RepairEvent[]>('/events/active', false);
	return events[0];
}
