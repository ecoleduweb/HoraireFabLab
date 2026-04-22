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
  plage: number;
  startAt: string;
  endAt: string;
  clientFname: string;
  clientLname: string;
  clientEmail: string;
  clientPhone: string;
  item: string;
  itemDescription: string;
  liabilityAccepted: boolean;
  isCanceled: false;
  updatedAt: string;
  createdAt: string;
}