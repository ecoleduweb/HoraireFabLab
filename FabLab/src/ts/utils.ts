import type { ValidationError } from "yup";
import type { ErrorResponse } from "../Models/ErrorResponse.ts"
import { POST } from "./server.ts"
import striptags from "striptags";

export const extractErrors = <T>(err: ValidationError): T => {
    return err.inner.reduce((acc: Record<string, string>, validationErr) => {
        return { ...acc, [validationErr.path ?? '']: validationErr.message }
    }, {}) as unknown as T
}

export const toFormattedDateString = (date: Date): string => {
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    return `${year}-${month}-${day}`
}


export const formatPhoneNumber = (phone: string): string => {
    // Supprime tous les caractères non numériques
    const cleaned = phone.replace(/\D/g, '');
    const match = cleaned.match(/^(\d{3})(\d{3})(\d{4})$/);
    if (match) {
        return `(${match[1]}) ${match[2]}-${match[3]}`;
    }
    return phone;
};

export const getShortURL = (url: string) => {
    try {
        const { hostname } = new URL(url);
        return hostname;
    } catch (e) {
        return url;
    }
};

export const isObjectEmpty = (obj: any) => {
    return !obj || Object.keys(obj).length === 0;
}

// TODO retirer ce bout de code lorsque les erreurs du back-end pourront être affichées au front-end
export const checkUrlAccessibility = async (url: string): Promise<boolean> => {
    try {
        const response = await POST<any, any>('/fablab/verifyURL', { url });
        return response.data.message === 'URL is accessible'
    } catch {
        return false;
    }
};

export const removeHtmlTags = (html: string): string => {
    return striptags(html);
};
