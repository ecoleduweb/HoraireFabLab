export interface TimeSlot {
  startAt:  string;   // ISO datetime ex : "2025-04-12T09:00:00"
  endAt:    string;
  label:     string;   
  available: number;
  capacity:  number;
}

export interface ReservationForm {
  firstName:       string;
  lastName:        string;
  email:           string;
  phone:           string;
  item:            string;
  itemDescription: string;
  waiverAccepted:  boolean;
}

export interface Reservation extends ReservationForm {
  plage:              number;   
  startAt:           string;   
  endAt:             string;   
  clientFname:       string;
  clientLname:       string;
  clientEmail:       string;
  clientPhone:       string;
  item:               string;
  itemDescription:   string;
  liabilityAccepted: boolean;
  isCanceled:        false;    
  updatedAt:         string;   
  createdAt:         string;   
}

export interface ReservationResponse {
  slotId:    number;
  startAt:   string;
  clientEmail: string;
}

export const emptyForm = (): ReservationForm => ({
  firstName:       "",
  lastName:        "",
  email:           "",
  phone:           "",
  item:            "",
  itemDescription: "",
  waiverAccepted:  false,
});

 
export interface DjangoSlotRaw {
  startAt:  string
  endAt:    string
  available: number
  capacity:  number
}
 
export interface DjangoEventResponse {
  id:         number
  name:       string
  eventDate: string   // "YYYY-MM-DD"
  plage: {
    id:    number
    slots: DjangoSlotRaw[]
  }
}
 
export interface EventData {
  id:         number
  name:       string
  eventDate: string
  plageId:    number
  slots:      TimeSlot[]
}