<script lang="ts">
  import { onMount } from 'svelte';

  import SlotGrid      from '../components/reservation/SlotGrid.svelte';
  import WaiverSection from '../components/reservation/WaiverSection.svelte';
  import Form          from '../components/reservation/Form.svelte';

  import type { TimeSlot }        from '../models/TimeSlot.ts';
  import type { RepairEvent }     from '../modelse/RepairEvent.ts';
  import type { ReservationForm } from '../modelse/Reservation.ts';

  import { reservationTemplate, validateReservationForm } from '../validatione/reservation.validation.ts';
  import { fetchActiveEvent, postReservation }            from '../services/ReservationService.ts';
  import { displayDate, displayTime }                     from '../ts/displayUtils.ts';
  import { InvalidDataError }                             from '../CustomError/invalidDataError.ts';
  import { NotFoundError }                                from '../CustomError/NotFoundError.ts';

  let eventData       = $state<RepairEvent>();
  let selectedStartAt = $state<string>('');
  let submitSuccess   = $state(false);
  let submitError     = $state<string | null>(null);
  let submittedValues = $state<ReservationForm | null>(null);

  const slots        = $derived(eventData?.slots ?? []);
  const selectedSlot = $derived(slots.find(s => s.startAt === selectedStartAt));

  onMount(async () => {
    eventData = await fetchActiveEvent();
  });

  function handleSlotSelect(slot: TimeSlot) {
    selectedStartAt = slot.startAt;
    setFields('slot', slot, true);
  }

  async function handleSubmit(values: ReservationForm) {
    submitError = null;

    if (!selectedSlot) {
      submitError = 'Veuillez choisir une plage horaire.';
      return;
    }

    try {
      await postReservation(values, selectedSlot);
      submittedValues = values;
      submitSuccess   = true;
    } catch (e: unknown) {
      if (e instanceof InvalidDataError) {
        submitError = 'Veuillez corriger les erreurs dans le formulaire.';
      } else if (e instanceof NotFoundError) {
        submitError = "Ce créneau n'existe plus. Veuillez en choisir un autre.";
      } else {
        submitError = e instanceof Error
          ? e.message
          : 'Une erreur est survenue. Veuillez réessayer.';
      }
    }
  }


  const { form: felteForm, errors, setFields } = validateReservationForm( handleSubmit,reservationTemplate.generate())
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
        {eventData.name} · {displayDate(eventData.eventDate)}
      </div>
    {/if}

    <p class="hero-sub">Réservez votre place. Aucun compte requis.</p>
  </div>

  <div class="content">

    {#if submitSuccess && submittedValues}
      <div class="alert-success" role="status">
        <h2>Réservation confirmée !</h2>
        <p>
          Merci <strong>{submittedValues.clientFname} {submittedValues.clientLname}</strong> !<br/>
          Plage réservée : <strong>{displayTime(submittedValues.slot!.startAt)}</strong>
          le <strong>{eventData ? displayDate(eventData.eventDate) : ''}</strong>.<br/>
          Courriel de confirmation envoyé à <strong>{submittedValues.clientEmail}</strong>.
        </p>
      </div>

    {:else}

      <form use:felteForm>

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
          <Form
            errors={$errors}
            {slots}
            {selectedStartAt}
            onSelectSlot={handleSlotSelect}
          />
        </div>

        <div class="section-bar"></div>
        <div class="section-head"><h2>3 — Décharge de responsabilité</h2></div>
        <div class="section-body">
          <WaiverSection error={$errors.waiverAccepted} />
        </div>

        {#if submitError}
          <div class="alert-error" role="alert">{submitError}</div>
        {/if}

        <button type="submit" class="btn-submit">
          Confirmer la réservation
        </button>
        <p class="note">Aucun compte requis · Données supprimées après l'événement</p>

      </form>

    {/if}
  </div>
</div>

<style>
  :global(:root) {
    --bg:    #0e1117;
    --card:  #161b24;
    --bord:  #2a3347;
    --white: #ffffff;
    --muted: #7a8599;
    --teal:  #00c9b1;
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

  .alert-error {
    padding: .85rem 1.1rem; margin-bottom: 1.25rem;
    border-radius: 3px;
    background: rgba(192,57,43,.12); border-left: 4px solid #c0392b;
    color: #e57373; font-size: .9rem;
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
    display: flex; align-items: center; justify-content: center;
  }
  .btn-submit:hover { filter: brightness(1.12); transform: translateY(-1px); }

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