export interface Reservation {
  plage:              number;   
  startAt:           string;   
  endAt:             string;   
  clientFname:       string;
  clientLname:       string;
  clientEmail:       string;
  clientPhone:       string;
  item:               string;
  itemDescription:   string;
  waiverAccepted: boolean;
  isCanceled:        false;    
  updatedAt:         string;   
  createdAt:         string;   
}


