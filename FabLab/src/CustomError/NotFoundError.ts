export class NotFoundError extends Error {
    constructor(message: string = "Ressource introuvable") {
        super(message)
        this.name = "NotFoundError"
    }
}