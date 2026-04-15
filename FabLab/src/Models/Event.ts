export interface Event {
    id: number
    name: string
    event_date: string
    created_at: string
}

export interface CreateEventPayload {
    name: string
    event_date: string
}