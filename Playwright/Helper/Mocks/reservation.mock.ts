import type { ReservationForm } from '../../../FabLab/src/models/Reservation';

export const MOCK_EVENT = {
  id:        1,
  name:      "Atelier Réparation",
  eventDate: "2026-07-16",
  createdAt: "2026-01-01T00:00:00",
  slots: [
    { startAt: "2026-07-16T08:00:00", endAt: "2026-07-16T08:15:00", capacity: 3 },
    { startAt: "2026-07-16T08:30:00", endAt: "2026-07-16T08:45:00", capacity: 3 },
  ],
};


export const VALID_FORM = {
  clientFname:     "Marie",
  clientLname:     "Tremblay",
  clientEmail:     "marie@example.com",
  clientPhone:     "514-555-0000",
  item:            "Grille-pain",
  itemDescription: "En panne depuis hier, le bouton de mise en marche est cassé",
  waiverAccepted:  true,
  slot:            MOCK_EVENT.slots[0],
};

export const EXPECTED_PAYLOAD: ReservationForm = {
  clientFname:     "Marie",
  clientLname:     "Tremblay",
  clientEmail:     "marie@example.com",
  clientPhone:     "514-555-0000",
  item:            "Grille-pain",
  itemDescription: "En panne depuis hier, le bouton de mise en marche est cassé",
  waiverAccepted:  true,
  slot:            MOCK_EVENT.slots[0],
};


export const MOCK_BOOK_SUCCESS = {
  slot_id:     99,
  startAt:     "2026-07-16T08:00:00",
  clientEmail: "marie@example.com",
};