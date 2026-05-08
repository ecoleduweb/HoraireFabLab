export function displayTime(iso: string): string {
    const [, time] = iso.split('T')
    const [h, m] = time.split(':')
    return `${parseInt(h)} h ${m}`
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