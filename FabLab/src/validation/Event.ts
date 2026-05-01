import * as yup from 'yup';
import { createForm } from 'felte';
import type { EventFormValues } from '../forms/event.ts';

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

export const validateEventForm = (handleSubmit: (values: EventFormValues) => void) => {
	return createForm<EventFormValues>({
		initialValues: { name: '', eventDate: '' },
		validate: async (values: EventFormValues) => {
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
