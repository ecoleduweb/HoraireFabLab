export interface EventFormValues {
    name: string;
    eventDate: string;
}

export const eventTemplate = {
    generate: (): EventFormValues => ({
        name: '',
        eventDate: '',
    })
};