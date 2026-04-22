<script lang="ts">
 
  import type { ReservationForm } from "../../models/Reservation.ts";
  import { validateField , type FormErrors} from "../../validation/reservation.validation.ts";

  interface Props {
    form:   ReservationForm;
    errors: FormErrors;
  }

  let { form = $bindable(), errors = $bindable() }: Props = $props();

  async function onBlur(field: keyof ReservationForm) {
    const msg = await validateField(field, form[field]);
    errors = { ...errors, [field]: msg };
  }
</script>

<div class="grid">

  <div class="field">
    <label for="firstName">
      Prénom <span class="req">*</span>
    </label>
    <input
      id="firstName" type="text"
      bind:value={form.firstName}
      onblur={() => onBlur('firstName')}
      placeholder="Marie"
      autocomplete="given-name"
      class:invalid={!!errors.firstName}
    />
    {#if errors.firstName}<span class="err">{errors.firstName}</span>{/if}
  </div>

  <div class="field">
    <label for="lastName">
      Nom <span class="req">*</span>
    </label>
    <input
      id="lastName" type="text"
      bind:value={form.lastName}
      onblur={() => onBlur('lastName')}
      placeholder="Tremblay"
      autocomplete="family-name"
      class:invalid={!!errors.lastName}
    />
    {#if errors.lastName}<span class="err">{errors.lastName}</span>{/if}
  </div>

  <div class="field">
    <label for="email">
      Courriel <span class="req">*</span>
    </label>
    <input
      id="email" type="email"
      bind:value={form.email}
      onblur={() => onBlur('email')}
      placeholder="marie@exemple.com"
      autocomplete="email"
      class:invalid={!!errors.email}
    />
    {#if errors.email}<span class="err">{errors.email}</span>{/if}
  </div>

  <div class="field">
    <label for="phone">Téléphone</label>
    <input
      id="phone" type="tel"
      bind:value={form.phone}
      onblur={() => onBlur('phone')}
      placeholder="514 555-0000"
      autocomplete="tel"
      class:invalid={!!errors.phone}
    />
    {#if errors.phone}<span class="err">{errors.phone}</span>{/if}
  </div>

  <div class="field full">
    <label for="item">
      Nom de l'objet <span class="req">*</span>
    </label>
    <input
      id="item" type="text"
      bind:value={form.item}
      onblur={() => onBlur('item')}
      placeholder="ex : Grille-pain Cuisinart CPT-122"
      class:invalid={!!errors.item}
    />
    {#if errors.item}<span class="err">{errors.item}</span>{/if}
  </div>

  <div class="field full">
    <label for="itemDescription">
      Description du bris <span class="req">*</span>
    </label>
    <textarea
      id="itemDescription"
      bind:value={form.itemDescription}
      onblur={() => onBlur('itemDescription')}
      rows="4"
      placeholder="ex : Ne chauffe plus, bouton coincé, câble effiloché…"
      class:invalid={!!errors.itemDescription}
    ></textarea>
    {#if errors.itemDescription}<span class="err">{errors.itemDescription}</span>{/if}
  </div>

</div>

<style>
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
    font-size: .68rem; color: #e8455a; margin-top: 1px;
  }
</style>