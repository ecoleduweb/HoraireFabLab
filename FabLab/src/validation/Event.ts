import * as yup from 'yup';
import { createForm } from 'felte';
import type { Event } from '../models/Event.ts';

export const eventSchema = yup.object().shape({
	name: yup
		.string()
		.required('Le nom est requis.')
		.max(100, 'Le nom ne doit pas dépasser 100 caractères.'),
	eventDate: yup
		.string()
		.required('La date est requise.')
		.matches(/^\d{4}-\d{2}-\d{2}$/, 'Le format de la date doit être AAAA-MM-JJ.')
});

export const validateEventForm = (handleSubmit: (values: Event) => void, event: Event) => {
	return createForm({
		initialValues: { ...event },
		validate: async (values: Event) => {
			try {
				await eventSchema.validate(values, { abortEarly: false });
				return {};
			} catch (err: unknown) {
				if (err instanceof yup.ValidationError) {
					const errors: Record<string, string> = {};
					err.inner.forEach((e: yup.ValidationError) => {
						errors[e.path!] = e.message;
					});
					if (Object.keys(errors).length === 0 && err.path) {
						errors[err.path] = err.message;
					}
					return errors;
				}
				return {};
			}
		},
		onSubmit: handleSubmit
	});
};
