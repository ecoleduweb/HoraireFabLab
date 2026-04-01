<script lang="ts">
    import { page } from '$app/state';
    import { icons } from '../../lib/icon.ts';

    const navItems = [
        { label: 'Événements',     href: '/admin/events',       icon: icons.calendar },
        { label: 'Plages horaires', href: '/admin/timeslots',   icon: icons.clock    },
        { label: 'Réservations',   href: '/admin/reservations', icon: icons.ticket   },
    ];

    function isActive(href: string): boolean {
        return page.url.pathname.startsWith(href);
    }
</script>

<aside class="sidebar">
    <div class="sidebar-logo">
        <a href="/admin" class="logo-link">
            <span class="logo-name">HoraireFabLab</span>
            <span class="logo-sub">Administration</span>
        </a>
    </div>

    <nav class="sidebar-nav">
        {#each navItems as item}
            <a href={item.href} class="nav-item" class:active={isActive(item.href)}>
                <span class="nav-icon">{@html item.icon}</span>
                {item.label}
            </a>
        {/each}
    </nav>
</aside>

<style>
    .sidebar {
        width: 220px;
        flex-shrink: 0;
        background-color: #1e2634;
        display: flex;
        flex-direction: column;
        border-right: 1px solid rgba(255, 255, 255, 0.06);
    }

    .sidebar-logo {
        padding: 1.25rem 1rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    }

    .logo-link {
        display: flex;
        flex-direction: column;
        gap: 2px;
        text-decoration: none;
    }

    .logo-name {
        font-family: RobotoCondensed-Bold;
        font-size: 16px;
        color: #fff;
        letter-spacing: -0.2px;
    }

    .logo-sub {
        font-family: RobotoCondensed-Regular;
        font-size: 11px;
        color: rgba(255, 255, 255, 0.35);
        text-transform: uppercase;
        letter-spacing: 0.6px;
    }

    .sidebar-nav {
        display: flex;
        flex-direction: column;
        padding: 0.75rem 0.5rem;
        gap: 2px;
    }

    .nav-item {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 9px 0.75rem;
        font-family: RobotoCondensed-Regular;
        font-size: 14px;
        color: rgba(255, 255, 255, 0.5);
        border-radius: 8px;
        text-decoration: none;
        transition: background 0.15s, color 0.15s;
    }

    .nav-item:hover {
        background-color: rgba(255, 255, 255, 0.06);
        color: rgba(255, 255, 255, 0.85);
    }

    .nav-item.active {
        background-color: rgba(0, 173, 154, 0.15);
        color: #00ad9a;
        font-family: RobotoCondensed-Medium;
    }

    .nav-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }
</style>