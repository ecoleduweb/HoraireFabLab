import type { TimeSlot } from "../models/TimeSlot.ts";

export interface DjangoSlotRaw {
    startAt:  string
    endAt:    string
    available: number
    capacity:  number
}

/* GET /api/events/active/ */
export interface DjangoEventResponse {
    id:         number
    name:       string
    eventDate: string   
    plage: {
        id:    number
        slots: DjangoSlotRaw[]
    }
}

/* Forme  utilisée dans les composants Svelte */
export interface EventData {
    id:        number
    name:      string
    eventDate: string
    plageId:   number
    slots:     TimeSlot[]
}