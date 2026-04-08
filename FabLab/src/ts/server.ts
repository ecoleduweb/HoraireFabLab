import { env } from "$env/dynamic/public"
import { InvalidDataError } from "../CustomError/invalidDataError.ts"
import { NotFoundError } from "../CustomError/NotFoundError.ts"
import type { ReservationPayload, ReservationResponse, TimeSlot, DjangoSlotRaw, DjangoEventResponse, EventData } from "../models/Reservation.ts"


export async function GET<T>(url: string, redirectToLoginOn401?: boolean): Promise<T> {
    try {
        
        const response = await fetch(`${env.PUBLIC_BASE_URL}${url}`, {
            credentials: "include"
        })

        const data = await handleResponse<T>(response, redirectToLoginOn401)
        return data as T
    } catch (error) {
        console.error("Error fetching:", error)
        throw error
    }
}

export async function POST<T, T1>(url: string, body: T, redirectToLoginOn401?: boolean): Promise<{ data: T1 }> {
    try {
        const response = await fetch(`${env.PUBLIC_BASE_URL}${url}`, {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(body),
        })

        const data = await handleResponse<T1>(response, redirectToLoginOn401)
        return { data: data as T1 }
    } catch (error) {
        console.error("Error posting:", error)
        throw error
    }
}

export async function DELETE(url: string): Promise<void> {
    try {
        const response = await fetch(`${env.PUBLIC_BASE_URL}${url}`, {
            method: "DELETE",
            credentials: "include",
            headers: {
                "Content-Type": "application/json",
            },
        })
        await handleResponse(response)
    } catch (error) {
        console.error("Error deleting:", error)
        throw error
    }
}

export async function PUT<T, T1>(url: string, body: T, redirectToLoginOn401?: boolean): Promise<{ data: T1 }> {
    try {
        const response = await fetch(`${env.PUBLIC_BASE_URL}${url}`, {
            method: "PUT",
            credentials: "include",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(body),
        })

        const data = await handleResponse<T1>(response, redirectToLoginOn401)
        return { data: data as T1 }
    } catch (error) {
        console.error("Error putting:", error)
        throw error
    }
}

export async function PATCH<T>(url: string, body: T): Promise<void> {
    try {
        const response = await fetch(`${env.PUBLIC_BASE_URL}${url}`, {
            method: "PATCH",
            credentials: "include",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(body),
        })

        await handleResponse(response)
    } catch (error) {
        console.error("Error patching:", error)
        throw error
    }
}


async function handleResponse<T>(response: Response, redirectToLoginOn401: boolean = true): Promise<T | undefined> {
    if (!response.ok) {
        if (response.status === 500 && redirectToLoginOn401) {
            window.location.href = "/500"
        } else if (response.status === 404) {
                throw new NotFoundError()
        } else if (response.status === 401 && redirectToLoginOn401) {
            window.location.href = "/login"
        } else if (response.status === 400) {
            const data = await response.json();
            if (data.field && data.message) {
                throw new InvalidDataError(data.message, data.field);
            } else {
                throw new Error(data.detail || data.message || `Error: ${response.status} - ${response.statusText}`)
            }
        } else {
            throw new Error(`Error: ${response.status} - ${response.statusText}`)
        }
    }
    return (await response.json()) as T
}

// Routes backend attendues :
//   GET  /api/events/active/   DjangoEventResponse
//   POST /api/slots/reserve/   ReservationResponse
 
/** ISO datetime ex "9 h 00" */
function toLabel(iso: string): string {
    const d = new Date(iso)
    const h = d.getHours()
    const m = d.getMinutes().toString().padStart(2, "0")
    return `${h} h ${m}`
}
 
function mapEvent(data: DjangoEventResponse): EventData {
    return {
        id:         data.id,
        name:       data.name,
        event_date: data.event_date,
        plageId:    data.plage.id,
        slots:      data.plage.slots.map(s => ({
            start_at:  s.start_at,
            label:     toLabel(s.start_at),
            available: s.available,
            capacity:  s.capacity,
        })),
    }
}
 
/**
 * Récupère l'événement actif et ses créneaux groupés.
 * GET /api/events/active/
 * pas de redirection sur 401 (false).
 */
export async function fetchActiveEvent(): Promise<EventData> {
    const raw = await GET<DjangoEventResponse>("/api/events/active/", false)
    return mapEvent(raw)
}
 
/**
 * Soumet une réservation.
 * POST /api/slots/reserve/
 * Le backend assigne le premier Slot libre pour ce start_at.
 * En cas de 400 avec { field, message } InvalidDataError (handleResponse).
 *  pas de redirection sur 401 (false).
 */
export async function postReservation(payload: ReservationPayload): Promise<ReservationResponse> {
    const { data } = await POST<ReservationPayload, ReservationResponse>(
        "/api/slots/reserve/",
        payload,
        false
    )
    return data
}