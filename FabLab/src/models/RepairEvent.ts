import type { TimeSlot } from './TimeSlot.ts';

export interface RepairEvent extends EventForm {
	id: number;
	createdAt: string;
	slots: TimeSlot[];
}

export interface EventForm {
	name: string;
	eventDate: string;
}
export interface UpdateRepairEvent extends EventForm {
	id: number;
}
