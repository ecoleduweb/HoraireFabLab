export interface TimeSlot {
  start_at:  string;   // ISO datetime ex : "2025-04-12T09:00:00"
  end_at:    string;
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
  start_at:           string;   
  end_at:             string;   
  client_fname:       string;
  client_lname:       string;
  client_email:       string;
  client_phone:       string;
  item:               string;
  item_description:   string;
  liability_accepted: boolean;
  is_canceled:        false;    
  updated_at:         string;   
  created_at:         string;   
}

export interface ReservationResponse {
  slot_id:    number;
  start_at:   string;
  client_email: string;
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
  start_at:  string
  end_at:    string
  available: number
  capacity:  number
}
 
export interface DjangoEventResponse {
  id:         number
  name:       string
  event_date: string   // "YYYY-MM-DD"
  plage: {
    id:    number
    slots: DjangoSlotRaw[]
  }
}
 
export interface EventData {
  id:         number
  name:       string
  event_date: string
  plageId:    number
  slots:      TimeSlot[]
}