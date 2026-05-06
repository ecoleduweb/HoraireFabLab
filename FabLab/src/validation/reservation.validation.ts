import { createForm } from 'felte'
import * as yup from 'yup'
import type { ReservationForm } from '../models/Reservation.ts'


const schema = yup.object().shape({
    clientFname: yup
        .string()
        .trim()
        .required('Le prénom est requis.')
        .min(2, 'Le prénom doit comporter au moins 2 caractères.'),

    clientLname: yup
        .string()
        .trim()
        .required('Le nom est requis.')
        .min(2, 'Le nom doit comporter au moins 2 caractères.'),

    clientEmail: yup
        .string()
        .trim()
        .required('Le courriel est requis.')
        .email('Veuillez entrer une adresse courriel valide.'),

    // Téléphone optionnel — format canadien si fourni
    clientPhone: yup
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

    liabilityAccepted: yup
        .boolean()
        .oneOf([true], 'Vous devez accepter la décharge de responsabilité.'),
})

export type FormErrors = Partial<Record<keyof ReservationForm, string>>

export const validateReservationForm = (
    handleSubmit: (values: ReservationForm) => void,
    initialValues: ReservationForm
) => {
    return createForm<ReservationForm>({
        initialValues,
        validate: async (values: any) => {
            try {
                await schema.validate(values, { abortEarly: false })
                return {}
            } catch (err) {
                const errors: FormErrors = {}
                if (err instanceof yup.ValidationError) {
                    err.inner.forEach((e) => {
                        if (e.path) errors[e.path as keyof ReservationForm] = e.message
                    })
                }
                return errors
            }
        },
        onSubmit: handleSubmit,
    })
}

export const reservationTemplate = {
    generate: (): ReservationForm => ({
        clientFname:       "",
        clientLname:        "",
        clientEmail:           "",
        clientPhone:           "",
        item:            "",
        itemDescription: "",
        liabilityAccepted:  false,
        slot: undefined,
    })
};
