<script lang="ts">
    import { base } from '$app/paths';
    import { goto } from '$app/navigation';
    import { POST } from '../../../../ts/server.ts';
	import type { EventForm, RepairEvent } from '../../../../models/RepairEvent.ts';

    let name = $state('');
    let eventDate = $state('');
    let loading = $state(false);
    let errors = $state<Record<string, string>>({});

    async function handleSubmit() {
        errors = {};
        loading = true;

        try {
            await POST<EventForm, RepairEvent>('/events', { name, eventDate });
            await goto(`${base}/admin`);
        } catch (e: unknown) {
            if (e instanceof Error) {
                errors.general = e.message;
            }
        } finally {
            loading = false;
        }
    }
</script>

<div class="page-header">
    <a href="{base}/admin" class="back-link">
        ← Retour
    </a>
    <h1>Créer un événement</h1>
    <p class="page-desc">Remplissez les informations pour créer une nouvelle journée d'événement.</p>
</div>

<form onsubmit={(e) => { e.preventDefault(); handleSubmit(); }}>
    <div class="form-card">
        <div class="form-group">
            <label for="name">Nom de l'événement</label>
            <input
                id="name"
                type="text"
                bind:value={name}
                placeholder="ex: Journée portes ouvertes FabLab"
                class:input-error={errors.name}
                disabled={loading}
            />
            {#if errors.name}
                <span class="error-msg">{errors.name}</span>
            {/if}
        </div>

        <div class="form-group">
            <label for="event_date">Date</label>
            <input
                id="event_date"
                type="date"
                bind:value={eventDate}
                class:input-error={errors.eventDate}
                disabled={loading}
            />
            {#if errors.eventDate}
                <span class="error-msg">{errors.eventDate}</span>
            {/if}
        </div>

        {#if errors.general}
            <div class="error-banner">{errors.general}</div>
        {/if}

        <div class="form-actions">
            <a href="{base}/admin" class="btn-cancel">Annuler</a>
            <button 
                type="submit" 
                class="btn-submit" 
                disabled={loading || !name || !eventDate}
            >
                {loading ? 'Création...' : 'Créer l\'événement'}
            </button>
        </div>
    </div>
</form>

<style>
    /* ── En-tête ── */
    .back-link {
        display: inline-block;
        font-family: var(--fb);
        font-size: 13px;
        color: #888;
        text-decoration: none;
        margin-bottom: 0.75rem;
        transition: color 0.15s;
    }

    .back-link:hover {
        color: #00ad9a;
    }

    .page-header {
        margin-bottom: 2rem;
    }

    .page-header h1 {
        font-family: var(--fh); font-weight: 900;
        font-size: 28px;
        color: #333;
        margin: 0 0 6px;
    }

    .page-desc {
        font-family: var(--fb);
        font-size: 15px;
        color: #888;
        margin: 0;
    }

    /* ── Card formulaire ── */
    .form-card {
        background-color: #fff;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 2rem;
        max-width: 520px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.06);
    }

    /* ── Champs ── */
    .form-group {
        display: flex;
        flex-direction: column;
        gap: 6px;
        margin-bottom: 1.25rem;
    }

    .form-group label {
        font-family: var(--fb); font-weight: 500;
        font-size: 14px;
        color: #333;
    }

    .form-group input {
        padding: 9px 12px;
        border: 1px solid #ccc;
        border-radius: 8px;
        font-family: var(--fb);
        font-size: 14px;
        color: #333;
        background-color: #fff;
        transition: border-color 0.15s;
    }

    .form-group input:focus {
        outline: none;
        border-color: #00ad9a;
    }

    .form-group input:disabled {
        background-color: #f5f5f5;
        cursor: not-allowed;
    }

    .input-error {
        border-color: #e74c3c !important;
    }

    .error-msg {
        font-family: var(--fb);
        font-size: 12px;
        color: #e74c3c;
    }

    /* ── Erreur générale ── */
    .error-banner {
        background-color: #fff5f5;
        border: 1px solid #f5c6c6;
        border-radius: 8px;
        padding: 10px 14px;
        font-family: var(--fb);
        font-size: 13px;
        color: #c0392b;
        margin-bottom: 1.25rem;
    }

    /* ── Actions ── */
    .form-actions {
        display: flex;
        gap: 12px;
        justify-content: flex-end;
        margin-top: 1.5rem;
        padding-top: 1.25rem;
        border-top: 1px solid #f0f0f0;
    }

    .btn-cancel {
        padding: 9px 18px;
        border: 1px solid #ccc;
        border-radius: 8px;
        font-family: var(--fb); font-weight: 500;
        font-size: 14px;
        color: #666;
        text-decoration: none;
        transition: all 0.15s;
    }

    .btn-cancel:hover {
        background-color: #f5f5f5;
        color: #333;
    }

    .btn-submit {
        padding: 9px 20px;
        border: none;
        border-radius: 14px;
        font-family: var(--fb); font-weight: 500;
        font-size: 16px;
        color: white;
        cursor: pointer;
        transition: 0.5s;
        background: linear-gradient(
            90deg,
            var(--c1, #329b8d),
            var(--c2, #37ad9a) 45%,
            var(--c3, #992050) 60%,
            var(--c4, #ab223a) 85%
        ) var(--x, 0) / 200%;
    }

    .btn-submit:hover:not(:disabled) {
        --x: 100%;
    }

    .btn-submit:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }
</style>