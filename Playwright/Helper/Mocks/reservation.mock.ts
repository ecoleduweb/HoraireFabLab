import type { Reservation } from "../types.ts";

export const MOCK_EVENT = {
  id: 1,
  name: "Atelier Réparation",
  eventDate: "2026-07-16",
  plage: {
    id: 1,
    slots: [
      { startAt: "2026-07-16T08:00:00", endAt: "2026-07-16T08:15:00", available: 2, capacity: 3 },
      { startAt: "2026-07-16T08:30:00", endAt: "2026-07-16T08:45:00", available: 0, capacity: 3 }
    ]
  }
};

export const EXPECTED_PAYLOAD: Omit<Reservation, "updatedAt" | "createdAt"> = {
  plage: 1,
  startAt: "2026-07-16 08:00:00",
  endAt: "2026-07-16 08:15:00",
  clientFname: "Marie",
  clientLname: "Tremblay",
  clientEmail: "marie@example.com",
  clientPhone: "514-555-0000",
  item: "Grille-pain",
  itemDescription: "En panne depuis hier, le bouton de mise en marche est cassé",
  liabilityAccepted: true,
  isCanceled: false
};