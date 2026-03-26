import { env } from "$env/dynamic/public"
import { InvalidDataError } from "../CustomError/invalidDataError.ts"

export async function GET<T>(url: string, redirectToLoginOn401?: boolean): Promise<T> {
    try {
        
        const response = await fetch(`${env.PUBLIC_BASE_URL}${url}`, {
            credentials: "include"
        })

        const data = await handleResponse<T>(response, redirectToLoginOn401)
        return data as T
    } catch (error) {
        console.error("Error fetching:", error)
        throw error
    }
}

export async function POST<T, T1>(url: string, body: T, redirectToLoginOn401?: boolean): Promise<{ data: T1 }> {
    var response


    try {
        const response = await fetch(`${env.PUBLIC_BASE_URL}${url}`, {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(body),
        })

        const data = await handleResponse<T1>(response, redirectToLoginOn401)
        return { data: data as T1 }
    } catch (error) {
        console.error("Error posting:", error)
        throw error
    }
}

export async function DELETE(url: string): Promise<void> {
    try {
        const response = await fetch(`${env.PUBLIC_BASE_URL}${url}`, {
            method: "DELETE",
            credentials: "include",
            headers: {
                "Content-Type": "application/json",
            },
        })
        await handleResponse(response)
    } catch (error) {
        console.error("Error deleting:", error)
        throw error
    }
}

export async function PUT<T, T1>(url: string, body: T, redirectToLoginOn401?: boolean): Promise<{ data: T1 }> {
    try {
        const response = await fetch(`${env.PUBLIC_BASE_URL}${url}`, {
            method: "PUT",
            credentials: "include",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(body),
        })

        const data = await handleResponse<T1>(response, redirectToLoginOn401)
        return { data: data as T1 }
    } catch (error) {
        console.error("Error putting:", error)
        throw error
    }
}

export async function PATCH<T>(url: string, body: T): Promise<void> {
    try {
        const response = await fetch(`${env.PUBLIC_BASE_URL}${url}`, {
            method: "PATCH",
            credentials: "include",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(body),
        })

        await handleResponse(response)
    } catch (error) {
        console.error("Error patching:", error)
        throw error
    }
}


async function handleResponse<T>(response: Response, redirectToLoginOn401: boolean = true): Promise<T | undefined> {
    if (!response.ok) {
        if (response.status === 500 && redirectToLoginOn401) {
            window.location.href = "/500"
        } else if (response.status === 404) {
            throw new Error(`Error: 404 - Not Found`)
        } else if (response.status === 401 && redirectToLoginOn401) {
            window.location.href = "/login"
        } else if (response.status === 400) {
            const data = await response.json();
            if (data.field && data.message) {
                throw new InvalidDataError(data.message, data.field);
            } else {
                throw new Error(data.detail || data.message || `Error: ${response.status} - ${response.statusText}`)
            }
        } else {
            throw new Error(`Error: ${response.status} - ${response.statusText}`)
        }
    }
    return (await response.json()) as T
}