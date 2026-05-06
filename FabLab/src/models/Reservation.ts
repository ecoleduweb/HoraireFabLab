import type { TimeSlot } from "./TimeSlot.ts";

export interface Reservation extends ReservationForm {
  startAt:           string;   
  endAt:             string;   
  isCanceled:        false;    
  updatedAt:         string;   
  createdAt:         string;
}

export interface ReservationForm {
    clientFname:       string;
    clientLname:       string;
    clientEmail:       string;
    clientPhone:       string;
    item:               string;
    itemDescription:   string;
    liabilityAccepted: boolean;
    slot?: TimeSlot;
}

