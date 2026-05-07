// export interface EventFormValues {
//     name: string;
//     eventDate: string;
// }

// export const eventTemplate = {
//     generate: (): EventFormValues => ({
//         name: '',
//         eventDate: '',
//     })
// };
import type { Event } from '../models/Event.ts';
export const eventTemplate = {
	generate: (): Event => ({
		id: 0,
		name: '',
		eventDate: '',
		createdAt: ''
	})
};
