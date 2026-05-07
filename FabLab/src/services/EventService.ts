import { GET, POST, PUT } from '../ts/server.ts';
import type { CreateEventPayload, Event, UpdateEventPayload } from '../models/Event.ts';

export const EventService = {
	async createEvent(name: string, eventDate: string): Promise<void> {
		await POST<CreateEventPayload, Event>('/events', { name, eventDate });
	},
	async getEvents(): Promise<Event[]> {
		return await GET<Event[]>('/events/all_events');
	},
	async updateEvent(eventId: number, name: string, eventDate: string): Promise<void> {
		await PUT<UpdateEventPayload, Event>(`/events/${eventId}/update_date`, {
			id: eventId,
			name,
			eventDate
		});
	},
	async getEventById(eventId: number): Promise<Event> {
		return await GET<Event>(`/events/${eventId}`);
	}
};
