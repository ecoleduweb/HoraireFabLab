import * as yup from 'yup';
import type { ReservationForm } from '../modeles/Reservation.ts';

export const reservationSchema = yup.object({
  firstName: yup
    .string()
    .trim()
    .required('Le prénom est requis.')
    .min(2, 'Le prénom doit comporter au moins 2 caractères.'),

  lastName: yup
    .string()
    .trim()
    .required('Le nom est requis.')
    .min(2, 'Le nom doit comporter au moins 2 caractères.'),

  email: yup
    .string()
    .trim()
    .required('Le courriel est requis.')
    .email('Veuillez entrer une adresse courriel valide.'),

  // Téléphone optionnel — si fourni, format canadien
  phone: yup
    .string()
    .trim()
    .optional()
    .matches(
      /^(\+?1[\s.-]?)?(\(?\d{3}\)?[\s.-]?)?\d{3}[\s.-]?\d{4}$/,
      'Numéro de téléphone invalide.'
    ),

  item: yup
    .string()
    .trim()
    .required("La description de l'objet est requise.")
    .min(3, "Veuillez décrire l'objet (min. 3 caractères)."),

  itemDescription: yup
    .string()
    .trim()
    .required('La description du bris est requise.')
    .min(10, 'Veuillez décrire le bris (min. 10 caractères).'),

  waiverAccepted: yup
    .boolean()
    .oneOf([true], 'Vous devez accepter la décharge de responsabilité.'),
});

export type FormErrors = Partial<Record<keyof ReservationForm, string>>;


export async function validateReservation(
  form: ReservationForm
): Promise<FormErrors> {
  try {
    await reservationSchema.validate(form, { abortEarly: false });
    return {};
  } catch (err) {
    if (err instanceof yup.ValidationError) {
      return err.inner.reduce<FormErrors>((acc, e) => {
        if (e.path) acc[e.path as keyof ReservationForm] = e.message;
        return acc;
      }, {});
    }
    throw err;
  }
}

export async function validateField(
  field: keyof ReservationForm,
  value: unknown
): Promise<string | undefined> {
  try {
    await reservationSchema.validateAt(field, { [field]: value });
    return undefined;
  } catch (err) {
    if (err instanceof yup.ValidationError) return err.message;
    throw err;
  }
}