<script lang="ts">
  import { onMount } from 'svelte';

  import SlotGrid       from '../Components/Reservation/SlotGrid.svelte'
  import ReservationForm from '../Components/Reservation/ReservationForm.svelte'
  import WaiverSection  from '../Components/Reservation/WaiverSection.svelte'

  import type {  ReservationForm as FormType, EventData } from "../models/Reservation.ts"
  import type { TimeSlot }                                from "../models/TimeSlot.ts"
  import { emptyForm }                                    from "../models/Reservation.ts"
  import type { FormErrors }                            from "../validation/reservation.validation.ts"
  import { validateReservation }                        from "../validation/reservation.validation.ts"
  import { fetchActiveEvent, postReservation }          from "../ts/server.ts"
  import { InvalidDataError }                           from "../CustomError/invalidDataError.ts"
  import { NotFoundError }                              from "../CustomError/NotFoundError.ts"

  let eventData       = $state<EventData | null>(null);
  let slots           = $state<TimeSlot[]>([]);
  let selectedStartAt = $state<string>('');

  let form:   FormType   = $state(emptyForm());
  let errors: FormErrors = $state({});

  let loading       = $state(true);
  let fetchError    = $state<string | null>(null);
  let submitting    = $state(false);
  let submitSuccess = $state(false);
  let submitError   = $state<string | null>(null);

  function formatDate(dateStr: string): string {
    const d = new Date(dateStr + 'T00:00:00');
    return d.toLocaleDateString('fr-CA', {
      weekday: 'long', day: 'numeric', month: 'long', year: 'numeric',
    });
  }

  const selectedSlot = $derived(slots.find(s => s.startAt === selectedStartAt));

  onMount(async () => {
    try {
      eventData = await fetchActiveEvent();
      slots     = eventData.slots;
    } catch (err) {
       console.error('Échec du chargement de l\'événement:', err);
      fetchError = "Impossible de charger l'événement. Veuillez réessayer.";
    } finally {
      loading = false;
    }
  });

  function handleSlotSelect(slot: TimeSlot) {
    selectedStartAt = slot.startAt;
  }

  async function handleSubmit() {
    submitError = null;

    if (!selectedSlot) {
      submitError = 'Veuillez choisir une plage horaire.';
      return;
    }

    errors = await validateReservation(form);
    if (Object.keys(errors).length > 0) {
      submitError = 'Veuillez corriger les erreurs dans le formulaire.';
      return;
    }

    submitting = true;
    try {
      // AJUSTEMENT : On passe les objets requis par postReservation
      await postReservation(
        form, 
        selectedSlot, 
        eventData!.plageId
      );

      // Mise à jour locale de la disponibilité
      slots = slots.map(s =>
        s.startAt === selectedStartAt
          ? { ...s, available: Math.max(0, s.available - 1) }
          : s
      );

      submitSuccess = true;
    } catch (e: unknown) {
      if (e instanceof InvalidDataError) {
        // Mapping des erreurs backend vers le state local
        errors = { ...errors, [e.field as keyof FormType]: e.message }
        submitError = 'Veuillez corriger les erreurs dans le formulaire.'
      } else if (e instanceof NotFoundError) {
        submitError = 'Ce créneau n\'existe plus. Veuillez en choisir un autre.'
      } else {
        submitError = e instanceof Error
          ? e.message
          : 'Une erreur est survenue. Veuillez réessayer.'
      }
    } finally {
      submitting = false;
    }
  }
</script>

<svelte:head>
  <title>Réserver — FabLab Fabbulle</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="" />
  <link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700;800&family=Barlow:wght@400;500;600&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet" />
</svelte:head>

<div class="page">
  <div class="topbar">
    <span class="logo">FabLab <em>Fabbulle</em></span>
  </div>

  <div class="hero">
    <h1 class="hero-title">Atelier de <em>réparation</em><br/>FabLab Fabbulle</h1>

    {#if eventData}
      <div class="event-badge">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
          <path d="M19 3h-1V1h-2v2H8V1H6v2H5C3.9 4 3 4.9 3 6v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 16H5V9h14v10zM7 11h5v5H7z"/>
        </svg>
        {eventData.name} · {formatDate(eventData.eventDate)}
      </div>
    {/if}

    <p class="hero-sub">Réservez votre place. Aucun compte requis.</p>
  </div>

  <div class="content">
    {#if loading}
      <div class="loading">
        <div class="spinner"></div>
        Chargement de l'événement…
      </div>

    {:else if fetchError}
      <div class="alert-error" role="alert">
        {fetchError}
        <button onclick={() => location.reload()}>Réessayer</button>
      </div>

    {:else if submitSuccess}
      <div class="alert-success" role="status">
        <h2>Réservation confirmée !</h2>
        <p>
          Merci <strong>{form.firstName} {form.lastName}</strong> !<br/>
          Plage réservée : <strong>{selectedSlot?.label}</strong>
          le <strong>{eventData ? formatDate(eventData.eventDate) : ''}</strong>.<br/>
          Courriel de confirmation envoyé à <strong>{form.email}</strong>.
        </p>
      </div>

    {:else}
      <div class="section-bar"></div>
      <div class="section-head"><h2>1 — Choisissez une plage horaire</h2></div>
      <div class="section-body">
        <SlotGrid
          {slots}
          {selectedStartAt}
          onSelect={handleSlotSelect}
        />
      </div>

      <div class="section-bar"></div>
      <div class="section-head"><h2>2 — Vos informations et l'objet à réparer</h2></div>
      <div class="section-body">
        <ReservationForm bind:form bind:errors />
      </div>

      <div class="section-bar"></div>
      <div class="section-head"><h2>3 — Décharge de responsabilité</h2></div>
      <div class="section-body">
        <WaiverSection
          bind:accepted={form.waiverAccepted}
          error={errors.waiverAccepted}
        />
      </div>

      {#if submitError}
        <div class="alert-error" role="alert">{submitError}</div>
      {/if}

      <button class="btn-submit" onclick={handleSubmit} disabled={submitting} aria-busy={submitting}>
        {#if submitting}
          <div class="spinner-sm"></div> Envoi en cours…
        {:else}
          Confirmer la réservation
        {/if}
      </button>
      <p class="note">Aucun compte requis · Données supprimées après l'événement</p>
    {/if}
  </div>
</div>

<style>
  /* Tes styles CSS originaux ici... */
  :global(:root) {
    --bg:     #0e1117;
    --card:   #161b24;
    --bord:   #2a3347;
    --white: #ffffff;
    --muted: #7a8599;
    --teal:   #00c9b1;
    --fh: 'Barlow Condensed', 'Arial Narrow', Arial, sans-serif;
    --fb: 'Barlow', Arial, sans-serif;
    --fm: 'JetBrains Mono', monospace;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }

  .page {
    min-height: 100vh;
    background: var(--bg);
    font-family: var(--fb);
    color: var(--white);
  }

  .topbar {
    background: var(--card);
    border-bottom: 3px solid transparent;
    border-image: linear-gradient(to right, #7b1a2e, #c0392b, #e8455a, #c0392b, #7b1a2e) 1;
    padding: .75rem 2.5rem;
  }
  .logo {
    font-family: var(--fh); font-size: 1.1rem; font-weight: 700;
    letter-spacing: .08em; text-transform: uppercase; color: var(--white);
  }
  .logo em { color: var(--teal); font-style: normal; }

  .hero {
    background: var(--card);
    padding: 2.5rem 2.5rem 2rem;
    border-bottom: 4px solid transparent;
    border-image: linear-gradient(to right, #7b1a2e, #c0392b, #e8455a, #c0392b, #7b1a2e) 1;
  }
  .hero-title {
    font-family: var(--fh); font-size: clamp(1.6rem, 4vw, 2.6rem);
    font-weight: 800; text-transform: uppercase; letter-spacing: .04em; line-height: 1.1;
  }
  .hero-title em { color: var(--teal); font-style: normal; }
  .event-badge {
    display: inline-flex; align-items: center; gap: .5rem;
    margin-top: 1rem;
    background: rgba(0,201,177,.08); border: 1px solid rgba(0,201,177,.3);
    border-radius: 3px; padding: .4rem .9rem;
    font-family: var(--fm); font-size: .78rem; color: var(--teal);
  }
  .hero-sub { margin-top: .75rem; color: var(--muted); font-size: .9rem; line-height: 1.6; }

  .content { max-width: 860px; margin: 0 auto; padding: 2rem 1.5rem 4rem; }

  .section-bar { height: 4px; background: var(--teal); }
  .section-head {
    background: var(--card); padding: .7rem 1.2rem;
    border-bottom: 1px solid var(--bord);
  }
  .section-head h2 {
    font-family: var(--fh); font-size: .85rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: .12em; color: var(--white);
  }
  .section-body {
    background: var(--card); border: 1px solid var(--bord);
    border-top: none; padding: 1.4rem; margin-bottom: 1.5rem;
  }

  .loading {
    display: flex; flex-direction: column; align-items: center; gap: .75rem;
    padding: 3rem; color: var(--muted); font-family: var(--fm); font-size: .85rem;
  }
  .spinner {
    width: 28px; height: 28px;
    border: 3px solid var(--bord); border-top-color: var(--teal);
    border-radius: 50%; animation: spin .8s linear infinite;
  }
  @keyframes spin { to { transform: rotate(360deg); } }

  .alert-error {
    padding: .85rem 1.1rem; margin-bottom: 1.25rem;
    border-radius: 3px;
    background: rgba(192,57,43,.12); border-left: 4px solid #c0392b;
    color: #e57373; font-size: .9rem; display: flex;
    align-items: center; justify-content: space-between; gap: 1rem;
  }
  .alert-error button {
    padding: .3rem .8rem; background: #c0392b; color: #fff;
    border: none; border-radius: 3px; cursor: pointer; font-size: .8rem;
    flex-shrink: 0;
  }
  .alert-success {
    background: rgba(0,201,177,.08); border: 1px solid var(--teal);
    border-radius: 3px; color: var(--white);
    text-align: center; padding: 2.5rem 2rem; margin-bottom: 1.5rem;
  }
  .alert-success h2 {
    font-family: var(--fh); font-size: 1.6rem; font-weight: 800;
    text-transform: uppercase; letter-spacing: .05em;
    color: var(--teal); margin-bottom: .5rem;
  }
  .alert-success p { color: var(--muted); line-height: 1.6; }
  .alert-success strong { color: var(--white); }

  .btn-submit {
    width: 100%; padding: .85rem;
    background: linear-gradient(135deg, #7b1a2e 0%, #c0392b 40%, #e8455a 70%, #9b2335 100%);
    color: var(--white); border: none; border-radius: 6px;
    font-family: var(--fh); font-size: 1rem; font-weight: 700;
    letter-spacing: .1em; text-transform: uppercase;
    cursor: pointer; transition: filter .15s, transform .1s;
    display: flex; align-items: center; justify-content: center; gap: .5rem;
  }
  .btn-submit:hover:not(:disabled) { filter: brightness(1.12); transform: translateY(-1px); }
  .btn-submit:disabled { opacity: .6; cursor: not-allowed; }
  .spinner-sm {
    width: 16px; height: 16px;
    border: 2px solid rgba(255,255,255,.3); border-top-color: #fff;
    border-radius: 50%; animation: spin .8s linear infinite;
  }

  .note {
    text-align: center; margin-top: .6rem;
    font-family: var(--fm); font-size: .68rem;
    color: var(--muted); letter-spacing: .05em;
  }

  @media (max-width: 600px) {
    .hero { padding: 1.5rem 1rem 1.25rem; }
    .section-body { padding: 1rem; }
  }
</style>