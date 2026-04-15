import type { Reservation } from "../types.ts";

export const MOCK_EVENT = {
  id: 1,
  name: "Atelier Réparation",
  event_date: "2026-07-16",
  plage: {
    id: 1,
    slots: [
      { start_at: "2026-07-16T08:00:00", end_at: "2026-07-16T08:15:00", available: 2, capacity: 3 },
      { start_at: "2026-07-16T08:30:00", end_at: "2026-07-16T08:45:00", available: 0, capacity: 3 }
    ]
  }
};

export const EXPECTED_PAYLOAD: Omit<Reservation, "updated_at" | "created_at"> = {
  plage: 1,
  start_at: "2026-07-16 08:00:00",
  end_at: "2026-07-16 08:15:00",
  client_fname: "Marie",
  client_lname: "Tremblay",
  client_email: "marie@example.com",
  client_phone: "514-555-0000",
  item: "Grille-pain",
  item_description: "En panne",
  liability_accepted: true,
  is_canceled: false
};