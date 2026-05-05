<script lang="ts">

  import type { FormErrors }  from '../../validation/reservation.validation.ts';
  import type { TimeSlot }    from '../../models/TimeSlot.ts';
  import SlotGrid             from './SlotGrid.svelte';

  interface Props {
    errors:          FormErrors;
    slots:           TimeSlot[];
    selectedStartAt: string;
    onSelectSlot:    (slot: TimeSlot) => void;
  }

  let { errors, slots, selectedStartAt, onSelectSlot }: Props = $props();
</script>

<!-- ── Créneaux horaires ── -->
<div class="field full section-slots">
  <label class="section-label">Plage horaire <span class="req">*</span></label>
  <SlotGrid
    {slots}
    {selectedStartAt}
    onSelect={onSelectSlot}
  />
  {#if errors.slot}
    <span class="err">{errors.slot}</span>
  {/if}
</div>

<!-- ── Informations visiteur ── -->
<div class="grid">

  <div class="field">
    <label for="firstName">Prénom <span class="req">*</span></label>
    <input
      id="firstName"
      name="clientFname"
      type="text"
      placeholder="Marie"
      autocomplete="given-name"
      class:invalid={!!errors.clientFname}
    />
    {#if errors.clientFname}<span class="err">{errors.clientFname}</span>{/if}
  </div>

  <div class="field">
    <label for="lastName">Nom <span class="req">*</span></label>
    <input
      id="lastName"
      name="clientLname"
      type="text"
      placeholder="Tremblay"
      autocomplete="family-name"
      class:invalid={!!errors.clientLname}
    />
    {#if errors.clientLname}<span class="err">{errors.clientLname}</span>{/if}
  </div>

  <div class="field">
    <label for="email">Courriel <span class="req">*</span></label>
    <input
      id="email"
      name="clientEmail"
      type="email"
      placeholder="marie@exemple.com"
      autocomplete="email"
      class:invalid={!!errors.clientEmail}
    />
    {#if errors.clientEmail}<span class="err">{errors.clientEmail}</span>{/if}
  </div>

  <div class="field">
    <label for="phone">Téléphone</label>
    <input
      id="phone"
      name="clientPhone"
      type="tel"
      placeholder="514 555-0000"
      autocomplete="tel"
      class:invalid={!!errors.clientPhone}
    />
    {#if errors.clientPhone}<span class="err">{errors.clientPhone}</span>{/if}
  </div>

  <div class="field full">
    <label for="item">Nom de l'objet <span class="req">*</span></label>
    <input
      id="item"
      name="item"
      type="text"
      placeholder="ex : Grille-pain"
      class:invalid={!!errors.item}
    />
    {#if errors.item}<span class="err">{errors.item}</span>{/if}
  </div>

  <div class="field full">
    <label for="itemDescription">Description du bris <span class="req">*</span></label>
    <textarea
      id="itemDescription"
      name="itemDescription"
      rows="4"
      placeholder="Décris le problème…"
      class:invalid={!!errors.itemDescription}
    ></textarea>
    {#if errors.itemDescription}<span class="err">{errors.itemDescription}</span>{/if}
  </div>

</div>

<style>
  .section-slots {
    margin-bottom: 1.5rem;
  }
  .section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: .68rem; font-weight: 600;
    letter-spacing: .1em; text-transform: uppercase;
    color: #ffffff;
    display: block;
    margin-bottom: .5rem;
  }

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
</style>