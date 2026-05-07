<script lang="ts">
    import { base } from '$app/paths';
    import { goto } from '$app/navigation';
    import { untrack } from 'svelte';
    import { validateEventForm } from '../../validation/Event.ts';
    import { EventService } from '../../services/EventService.ts';
    import { eventTemplate } from '../../forms/event.ts';
    import type { RepairEvent } from '../../models/RepairEvent.ts';

	
type Props = {
    repairEventToEdit: RepairEvent|null;
}
    let { repairEventToEdit }: Props = $props();
    
    let loading = $state(false);

let event = $derived<RepairEvent>(repairEventToEdit ? { ...repairEventToEdit } : eventTemplate.generate());
 
        
    const repairEditEvent = $derived(repairEventToEdit !== null);
    const handleSubmit = async () => {
        loading = true;
        try {
            if (repairEditEvent) {
                await EventService.updateEvent(event.id, event.name, event.eventDate);
            }
            else {
                await EventService.createEvent(event.name, event.eventDate);
            }
            await goto(`/admin`);
        } catch (e: unknown) {
            if (e instanceof Error) {
                alert(e.message);
            }
        } finally {
            loading = false;
        }
    };

    const { form, errors } = validateEventForm(handleSubmit, untrack(() => event));

  
</script>


<form use:form>
    <div class="form-card">
        <div class="form-group">
            <label for="name">Nom de l'événement</label>
            <input
                id="name"
                type="text"
                name="name"
                placeholder="ex: Journée portes ouvertes FabLab"
                class:input-error={$errors.name}
                disabled={loading}
                bind:value={event.name}
             
            />
            {#if $errors.name}
                <span class="error-msg">{$errors.name}</span>
            {/if}
        </div>

        <div class="form-group">
            <label for="event_date">Date</label>
            <input
                id="event_date"
                type="date"
                name="eventDate"
                class:input-error={$errors.eventDate}
                disabled={loading}
                bind:value={event.eventDate}
            />
            {#if $errors.eventDate}
                <span class="error-msg">{$errors.eventDate}</span>
            {/if}
        </div>

        <div class="form-actions">
            <a href="{base}/admin" class="btn-cancel">Annuler</a>
            <button type="submit" class="btn-submit" disabled={loading}>
  {loading
    ? (repairEditEvent ? 'Modification...' : 'Création...')
    : (repairEditEvent ? "Modifier l'événement" : "Créer l'événement")}
</button>
        </div>
    </div>
</form>

<style>


  
    .form-card {
        background-color: #fff;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 2rem;
        max-width: 520px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.06);
    }

  
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