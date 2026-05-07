<script lang="ts">
  import type { TimeSlot }      from '../../models/TimeSlot.ts';
  import type { ReservationForm } from '../../models/Reservation.ts';
  import { reservationTemplate, validateReservationForm } from '../../validation/reservation.validation.ts';
  import { postReservation }    from '../../services/ReservationService.ts';
  import { displayTime }        from '../../ts/displayUtils.ts';
  import { InvalidDataError }   from '../../customError/invalidDataError.ts';
  import { NotFoundError }      from '../../customError/NotFoundError.ts';
  import SlotGrid               from './SlotGrid.svelte';
  import WaiverSection          from './WaiverSection.svelte';
  interface Props {
    slots: TimeSlot[];
  }

  let { slots }: Props = $props();

  let selectedStartAt  = $state<string>('');
  let submitSuccess    = $state(false);
  let submitError      = $state<string | null>(null);
  let submittedValues  = $state<ReservationForm | null>(null);

  const selectedSlot = $derived(slots.find(s => s.startAt === selectedStartAt));

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

  const { form, errors, setFields } = validateReservationForm(
    handleSubmit,
    reservationTemplate.generate()
  );
</script>

<!-- ── Confirmation ── -->
{#if submitSuccess && submittedValues}
  <div class="alert-success" role="status">
    <h2>Réservation confirmée !</h2>
    <p>
      Merci <strong>{submittedValues.clientFname} {submittedValues.clientLname}</strong> !<br/>
      Plage réservée : <strong>{displayTime(submittedValues.slot!.startAt)}</strong>.<br/>
      Courriel de confirmation envoyé à <strong>{submittedValues.clientEmail}</strong>.
    </p>
  </div>

<!-- ── Formulaire ── -->
{:else}
  <form use:form>

    <div class="section-bar"></div>
    <div class="section-head"><h2>1 — Choisissez une plage horaire</h2></div>
    <div class="section-body">
      <div class="field full section-slots">
        <SlotGrid
          {slots}
          {selectedStartAt}
          onSelect={handleSlotSelect}
        />
        {#if $errors.slot}
          <span class="err">{$errors.slot}</span>
        {/if}
      </div>
    </div>

    <div class="section-bar"></div>
    <div class="section-head"><h2>2 — Vos informations</h2></div>
    <div class="section-body">
      <div class="grid">

        <div class="field">
          <label for="firstName">Prénom <span class="req">*</span></label>
          <input
            id="firstName"
            name="clientFname"
            type="text"
            placeholder="Marie"
            autocomplete="given-name"
            class:invalid={!!$errors.clientFname}
          />
          {#if $errors.clientFname}<span class="err">{$errors.clientFname}</span>{/if}
        </div>

        <div class="field">
          <label for="lastName">Nom <span class="req">*</span></label>
          <input
            id="lastName"
            name="clientLname"
            type="text"
            placeholder="Tremblay"
            autocomplete="family-name"
            class:invalid={!!$errors.clientLname}
          />
          {#if $errors.clientLname}<span class="err">{$errors.clientLname}</span>{/if}
        </div>

        <div class="field">
          <label for="email">Courriel <span class="req">*</span></label>
          <input
            id="email"
            name="clientEmail"
            type="email"
            placeholder="marie@exemple.com"
            autocomplete="email"
            class:invalid={!!$errors.clientEmail}
          />
          {#if $errors.clientEmail}<span class="err">{$errors.clientEmail}</span>{/if}
        </div>

        <div class="field">
          <label for="phone">Téléphone</label>
          <input
            id="phone"
            name="clientPhone"
            type="tel"
            placeholder="5145552222"
            autocomplete="tel"
            class:invalid={!!$errors.clientPhone}
          />
          {#if $errors.clientPhone}<span class="err">{$errors.clientPhone}</span>{/if}
        </div>

      </div>
    </div>

    <div class="section-bar"></div>
    <div class="section-head"><h2>3 — L'objet à réparer</h2>
      <ul class="hero-sub">Voici les types d'objets que nous acceptons : 
      <li>- Électrique et électronique divers </li>
      <li>- Informatique (ordinateurs lents, problèmes logiciels)</li>
      <li>- Vêtements</li>
      <li>- Pièces de plastiques cassées</li>
      <li>- Couteaux à aiguiser</li>
      <br>Nous refusons : Cellulaires et tablettes , fours micro-ondes, grille-pains, gros électro-ménagers, moteurs à essence.</ul></div>
    <div class="section-body">
      <div class="grid">

        <div class="field full">
          <label for="item">Nom de l'objet <span class="req">*</span></label>
          <input
            id="item"
            name="item"
            type="text"
            placeholder="ex : Grille-pain"
            class:invalid={!!$errors.item}
          />
          {#if $errors.item}<span class="err">{$errors.item}</span>{/if}
        </div>

        <div class="field full">
          <label for="itemDescription">Description du bris <span class="req">*</span></label>
          <textarea
            id="itemDescription"
            name="itemDescription"
            rows="4"
            placeholder="Décris le problème…"
            class:invalid={!!$errors.itemDescription}
          ></textarea>
          {#if $errors.itemDescription}<span class="err">{$errors.itemDescription}</span>{/if}
        </div>

      </div>
    </div>

    <div class="section-bar"></div>
    <div class="section-head"><h2>4 — Décharge de responsabilité</h2></div>
    <div class="section-body">
      <WaiverSection error={$errors.liabilityAccepted} />
    </div>

    <!-- Erreur globale -->
    {#if submitError}
      <div class="alert-error" role="alert">{submitError}</div>
    {/if}

    <button type="submit" class="btn-submit">
      Confirmer la réservation
    </button>
    <p class="note">Aucun compte requis · Données supprimées après l'événement</p>

  </form>
{/if}

<style>
  .section-bar { height: 4px; background: #00c9b1; }
  .section-head {
    background: #161b24; padding: .7rem 1.2rem;
    border-bottom: 1px solid #2a3347;
  }
  .section-head h2 {
    font-family: 'Barlow Condensed', 'Arial Narrow', Arial, sans-serif;
    font-size: .85rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: .12em; color: #ffffff;
  }
  .section-body {
    background: #161b24; border: 1px solid #2a3347;
    border-top: none; padding: 1.4rem; margin-bottom: 1.5rem;
  }

  .section-slots { margin-bottom: 0; }

  .grid { display: grid; grid-template-columns: 1fr 1fr; gap: .9rem; }
  @media (max-width: 520px) { .grid { grid-template-columns: 1fr; } }
  .full { grid-column: 1 / -1; }

  .field { display: flex; flex-direction: column; gap: .3rem; }

  label {
    font-family: 'JetBrains Mono', monospace;
    font-size: .68rem; font-weight: 600;
    letter-spacing: .1em; text-transform: uppercase;
    color: #ffffff;
  }
  .req { color: #00c9b1; margin-left: 2px; }

  input, textarea {
    width: 100%; padding: .6rem .85rem;
    background: #0e1117;
    border: 1px solid #2a3347;
    border-radius: 3px;
    font-family: 'Barlow', Arial, sans-serif;
    font-size: .95rem; color: #ffffff;
    outline: none; transition: border-color .15s;
  }
  input::placeholder, textarea::placeholder { color: #7a8599; }
  input:focus, textarea:focus {
    border-color: #00c9b1;
    box-shadow: 0 0 0 2px rgba(0,201,177,.12);
  }
  input.invalid, textarea.invalid { border-color: #e8455a; }
  textarea { resize: vertical; min-height: 80px; line-height: 1.5; }

  .err {
    font-family: 'JetBrains Mono', monospace;
    font-size: .68rem; color: #e8455a;
  }

  .alert-error {
    padding: .85rem 1.1rem; margin: 1rem 0;
    border-radius: 3px;
    background: rgba(192,57,43,.12); border-left: 4px solid #c0392b;
    color: #e57373; font-size: .9rem;
  }
  .alert-success {
    background: rgba(0,201,177,.08); border: 1px solid #00c9b1;
    border-radius: 3px; color: #ffffff;
    text-align: center; padding: 2.5rem 2rem;
  }
  .alert-success h2 {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1.6rem; font-weight: 800;
    text-transform: uppercase; color: #00c9b1; margin-bottom: .5rem;
  }
  .alert-success p { color: #7a8599; line-height: 1.6; }
  .alert-success strong { color: #ffffff; }

  .btn-submit {
    width: 100%; padding: .85rem; margin-top: 1.5rem;
    background: linear-gradient(135deg, #7b1a2e 0%, #c0392b 40%, #e8455a 70%, #9b2335 100%);
    color: #ffffff; border: none; border-radius: 6px;
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1rem; font-weight: 700;
    letter-spacing: .1em; text-transform: uppercase;
    cursor: pointer; transition: filter .15s, transform .1s;
    display: flex; align-items: center; justify-content: center;
  }
  .btn-submit:hover { filter: brightness(1.12); transform: translateY(-1px); }

  .note {
    text-align: center; margin-top: .6rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: .68rem; color: #7a8599; letter-spacing: .05em;
  }

  .hero-sub { font-family: 'Barlow Condensed', 'Arial Narrow', Arial, sans-serif; margin-top: .75rem; color: var(--white); font-size: .9rem; line-height: 1.6; }
</style>