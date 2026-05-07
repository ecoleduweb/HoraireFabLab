export function displayTime(iso: string): string {
    const d = new Date(iso)
    const h = d.getUTCHours()
    const m = d.getUTCMinutes().toString().padStart(2, "0")
    return `${h} h ${m}`
}

export function displayDate(dateStr: string): string {
    const d = new Date(dateStr + "T00:00:00")
    return d.toLocaleDateString("fr-CA", {
        weekday: "long",
        day:     "numeric",
        month:   "long",
        year:    "numeric",
    })
}