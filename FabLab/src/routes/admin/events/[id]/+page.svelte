<script lang="ts">
    import { base } from '$app/paths';
    import { goto } from '$app/navigation';
    import { page } from '$app/state';
    import { onMount } from 'svelte';
    import { EventService } from '../../../../services/EventService.ts';
    import type { Event } from '../../../../models/Event.ts';
    import CreateandModifyForm from '../../../../components/RepairEvent/CreateandModifyForm.svelte';

    const eventId = $derived(Number(page.params.id));
    let event = $state<Event | null>(null);

    onMount(async () => {
        try {
            event = await EventService.getEventById(eventId);
        } catch (error) {
            console.error('Erreur chargement événement', error);
        }
    });
</script>
<div class="page-header">
    <a href="/admin" class="back-link">
        ← Retour
    </a>
    <h1>Modifier un événement</h1>
    <p class="page-desc">Remplissez les informations pour modifier la journée d'événement.</p>
</div>


{#if event}
    <CreateandModifyForm eventToEdit={event} onSuccess={() => goto('/admin')} onClose={() => goto('/admin')} />
{:else}
    <p>Chargement...</p>
{/if}
<style>
  
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

   
</style>