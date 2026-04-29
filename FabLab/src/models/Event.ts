export interface Event {
    id: number
    name: string
    eventDate: string
    createdAt: string
}

export interface CreateEventPayload {
    name: string
    eventDate: string
}