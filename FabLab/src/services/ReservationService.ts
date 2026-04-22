import { GET, POST }            from "../ts/server.ts"
import type { ReservationForm } from "../models/ReservationForm.ts"
import type { Reservation }     from "../models/Reservation.ts"
import type { ReservationResponse } from "../models/ReservationResponse.ts"
import type { TimeSlot }        from "../models/TimeSlot.ts"
import type { EventData, DjangoEventResponse } from "../models/DjangoEvent.ts"


/** Formate une Date JS en "YYYY-MM-DD HH:mm:ss" attendu par Django */
function toDateTimeStr(d: Date): string {
    const pad = (n: number) => n.toString().padStart(2, "0")
    return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ` +
           `${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`
}

function mapEvent(data: DjangoEventResponse): EventData {
    return {
        id:       data.id,
        name:     data.name,
        eventDate: data.eventDate,
        plageId:  data.plage.id,
        slots:    data.plage.slots.map(s => ({
            startAt:   s.startAt,
            endAt:     s.endAt,
            label:     `${new Date(s.startAt).getHours()} h ${new Date(s.startAt).getMinutes().toString().padStart(2, "0")}`,
            available: s.available,
            capacity:  s.capacity,
        })),
    }
}

export async function fetchActiveEvent(): Promise<EventData> {
    const raw = await GET<DjangoEventResponse>("/api/events/active/", false)
    return mapEvent(raw)
}


export async function postReservation(
    form:    ReservationForm,
    slot:    TimeSlot,
    plageId: number
): Promise<ReservationResponse> {

    const now    = new Date()
    const nowStr = toDateTimeStr(now)

    const reservation: Reservation = {
        plage:             plageId,
        startAt:          toDateTimeStr(new Date(slot.startAt)),
        endAt:            toDateTimeStr(new Date(slot.endAt)),
        clientFname:      form.clientFname,
        clientLname:      form.clientLname,
        clientEmail:      form.clientEmail,
        clientPhone:      form.clientPhone,
        item:              form.item,
        itemDescription:  form.itemDescription,
        waiverAccepted: form.waiverAccepted,
        isCanceled:       false,
        updatedAt:        nowStr,
        createdAt:        nowStr,
    }

    const { data } = await POST<Reservation, ReservationResponse>(
        "/api/book_slot",
        reservation,
        false
    )
    return data
}