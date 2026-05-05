import { GET, POST }            from "../ts/server.ts"
import type { Reservation, ReservationForm }     from "../models/Reservation.ts"
import type { TimeSlot }        from "../models/TimeSlot.ts"
import type { RepairEvent } from "../models/RepairEvent.ts"

 async function fetchAvailableSlots(eventId: number) {
     return await GET(`/api/events/availableSlots/${eventId}/`)
 }

export async function postReservation(
    reservation:    ReservationForm,
    slot:    TimeSlot,
): Promise<Reservation> {

   reservation.slot = slot

    const { data } = await POST<ReservationForm, Reservation>(
        "/api/book_slot",
        reservation,
    )
    return data
}