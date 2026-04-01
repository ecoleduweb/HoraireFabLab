const ICON_ATTRS = `width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"`;
const ICON_ATTRS_SM = `width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"`;

export const icons = {
    calendar: `<svg ${ICON_ATTRS}>
        <rect x="3" y="5" width="18" height="17" rx="3" stroke="currentColor" stroke-width="1.6"/>
        <path d="M8 3v4M16 3v4M3 11h18" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>
    </svg>`,

    calendarAdd: `<svg ${ICON_ATTRS}>
        <rect x="3" y="5" width="18" height="17" rx="3" stroke="currentColor" stroke-width="1.6"/>
        <path d="M8 3v4M16 3v4M3 11h18" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>
        <path d="M12 15v4M10 17h4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>
    </svg>`,

    clock: `<svg ${ICON_ATTRS}>
        <circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.6"/>
        <path d="M12 7v5.5l3 3" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>
    </svg>`,

    ticket: `<svg ${ICON_ATTRS}>
        <path d="M3 9a1 1 0 0 1 1-1h16a1 1 0 0 1 1 1v2a2 2 0 0 0 0 4v2a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1v-2a2 2 0 0 0 0-4V9Z" stroke="currentColor" stroke-width="1.6"/>
    </svg>`,

    user: `<svg ${ICON_ATTRS}>
        <circle cx="12" cy="8" r="4" stroke="currentColor" stroke-width="1.6"/>
        <path d="M4 20c0-4.418 3.582-8 8-8s8 3.582 8 8" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>
    </svg>`,

    chevronRight: `<svg ${ICON_ATTRS_SM}>
        <path d="M6 3l5 5-5 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>`,
} as const;

export type IconName = keyof typeof icons;