export interface MockResponse {
    status: number;
    json: any;
    headers?: Record<string, string>;
}

export interface MockConfig {
    url: string;
    method?: string;
    response: MockResponse;
}

export interface Reservation {
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