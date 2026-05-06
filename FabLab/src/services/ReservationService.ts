import { GET, POST }            from "../ts/server.ts"
import type { Reservation, ReservationForm }     from "../models/Reservation.ts"
import type { TimeSlot }        from "../models/TimeSlot.ts"
 
export async function fetchAvailableSlots(eventId: number): Promise<TimeSlot[]> {
    return await GET<TimeSlot[]>(`/availableSlots/${eventId}`)
}

export async function postReservation(
    reservation: ReservationForm,
    slot:        TimeSlot,
): Promise<Reservation> {
 
  const { data } = await POST<any, Reservation>(
        "/book_slot",
        {
            ...reservation,
            startAt: slot.startAt,
            endAt:   slot.endAt,
        },
    )
    return data
}