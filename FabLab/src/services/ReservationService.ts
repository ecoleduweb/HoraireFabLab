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
 
    // Le serializer Django attend du snake_case 
    const payload = {
        plage:              slot.plageId,
        start_at:           slot.startAt,
        end_at:             slot.endAt,
        client_fname:       reservation.clientFname,
        client_lname:       reservation.clientLname,
        client_email:       reservation.clientEmail,
        client_phone:       reservation.clientPhone,
        item:               reservation.item,
        item_description:   reservation.itemDescription,
        liability_accepted: reservation.waiverAccepted,
    }
 
    const { data } = await POST<typeof payload, Reservation>(
        "/book_slot",
        payload,
    )
    return data
}