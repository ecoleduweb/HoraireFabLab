export interface ReservationForm {
    clientFname:       string;
    clientLname:       string;
    clientEmail:       string;
    clientPhone:       string;
    item:               string;
    itemDescription:   string;
    waiverAccepted: boolean;  
}

export const emptyForm = (): ReservationForm => ({
    clientFname:       "",
    clientLname:        "",
    clientEmail:           "",
    clientPhone:           "",
    item:            "",
    itemDescription: "",
    waiverAccepted:  false,
})