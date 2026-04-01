<script lang="ts">
     import type { TimeSlot } from "../Models/TimeSlot.ts"

  const eventName = "Atelier de réparation — Printemps 2025";
  const eventDate = "2025-04-12";

  // TODO : remplacer par fetch('/api/events/active/') quand le backend Django est prêt
  let slots = $state<TimeSlot[]>([
    { start_at: "2025-04-12T09:00:00", label: "9 h 00",  available: 2, capacity: 3 },
    { start_at: "2025-04-12T09:15:00", label: "9 h 15",  available: 3, capacity: 3 },
    { start_at: "2025-04-12T09:30:00", label: "9 h 30",  available: 0, capacity: 3 },
    { start_at: "2025-04-12T09:45:00", label: "9 h 45",  available: 1, capacity: 3 },
    { start_at: "2025-04-12T10:00:00", label: "10 h 00", available: 3, capacity: 3 },
    { start_at: "2025-04-12T10:15:00", label: "10 h 15", available: 2, capacity: 3 },
    { start_at: "2025-04-12T10:30:00", label: "10 h 30", available: 0, capacity: 3 },
    { start_at: "2025-04-12T10:45:00", label: "10 h 45", available: 3, capacity: 3 },
    { start_at: "2025-04-12T11:00:00", label: "11 h 00", available: 1, capacity: 3 },
    { start_at: "2025-04-12T11:15:00", label: "11 h 15", available: 2, capacity: 3 },
    { start_at: "2025-04-12T11:30:00", label: "11 h 30", available: 3, capacity: 3 },
    { start_at: "2025-04-12T11:45:00", label: "11 h 45", available: 0, capacity: 3 },
    { start_at: "2025-04-12T13:00:00", label: "13 h 00", available: 2, capacity: 3 },
    { start_at: "2025-04-12T13:15:00", label: "13 h 15", available: 3, capacity: 3 },
    { start_at: "2025-04-12T13:30:00", label: "13 h 30", available: 1, capacity: 3 },
    { start_at: "2025-04-12T13:45:00", label: "13 h 45", available: 3, capacity: 3 },
    { start_at: "2025-04-12T14:00:00", label: "14 h 00", available: 0, capacity: 3 },
    { start_at: "2025-04-12T14:15:00", label: "14 h 15", available: 2, capacity: 3 },
    { start_at: "2025-04-12T14:30:00", label: "14 h 30", available: 3, capacity: 3 },
    { start_at: "2025-04-12T14:45:00", label: "14 h 45", available: 1, capacity: 3 },
  ]);

  let selectedStartAt = $state<string>("");

  let form = $state({
    firstName:       "",
    lastName:        "",
    email:           "",
    phone:           "",
    item:            "",
    itemDescription: "",
    waiverAccepted:  false,
  });

  let submitSuccess = $state(false);
  let submitError   = $state<string | null>(null);

  const waiverText = `En participant à cet atelier de réparation organisé par le FabLab Fabbulle,
je reconnais avoir été informé(e) que les bénévoles présents ne sont pas des techniciens
professionnels certifiés. Je comprends que la réparation de mon objet n'est pas garantie
et que le FabLab Fabbulle ne pourra être tenu responsable de tout dommage supplémentaire
survenant pendant ou après l'atelier. Je participe à cet événement volontairement et en
pleine connaissance de ces conditions.`;

  function formatDate(dateStr: string): string {
    const d = new Date(dateStr + "T00:00:00");
    return d.toLocaleDateString("fr-CA", { weekday: "long", day: "numeric", month: "long", year: "numeric" });
  }

  const selectedSlot = $derived(slots.find(s => s.start_at === selectedStartAt));

  function selectSlot(slot: TimeSlot) {
    if (slot.available === 0) return;
    selectedStartAt = slot.start_at;
  }

  function handleSubmit() {
    submitError = null;
    if (!selectedStartAt) {
      submitError = "Veuillez choisir une plage horaire.";
      return;
    }
    if (!form.waiverAccepted) {
      submitError = "Vous devez accepter la décharge de responsabilité.";
      return;
    }
    // TODO : appel API Django

    slots = slots.map(s =>
      s.start_at === selectedStartAt
        ? { ...s, available: Math.max(0, s.available - 1) }
        : s
    );
    submitSuccess = true;
  }
</script>

<svelte:head>
  <title>Réserver — FabLab Fabbulle</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="" />
  <link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700;800&family=Barlow:wght@400;500;600&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet" />
</svelte:head>


<div class="page">

  <!-- Topbar -->
  <div class="topbar">
    <span class="logo">FabLab <em>Fabbulle</em></span>
  </div>

  <!-- Hero -->
  <div class="hero">
    <h1 class="hero-title">Atelier de <em>réparation</em><br/>FabLab Fabbulle</h1>
    <div class="event-badge">
      {eventName} · {formatDate(eventDate)}
    </div>
    <p class="hero-sub">Réservez votre place. Aucun compte requis.</p>
  </div>

  <div class="content">

    {#if submitSuccess}
      <div class="alert-success">
        <h2>Réservation confirmée !</h2>
        <p>
          Merci <strong>{form.firstName} {form.lastName}</strong> !<br/>
          Plage réservée : <strong>{selectedSlot?.label}</strong> — {formatDate(eventDate)}.<br/>
          Courriel de confirmation envoyé à <strong>{form.email}</strong>.
        </p>
      </div>

    {:else}

      <!-- 1. Plage horaire -->
      <div class="section-bar"></div>
      <div class="section-head"><h2>1 — Choisissez une plage horaire</h2></div>
      <div class="section-body">

        {#if selectedSlot}
          <div class="slot-recap" role="status">
            Sélectionné : <strong>{selectedSlot.label}</strong>
            &nbsp;·&nbsp;{selectedSlot.available} place{selectedSlot.available > 1 ? 's' : ''} restante{selectedSlot.available > 1 ? 's' : ''}
          </div>
        {/if}

        <div class="slots-grid" role="group" aria-label="Créneaux disponibles">
          {#each slots as slot (slot.start_at)}
            <button
              class="slot-btn"
              class:selected={selectedStartAt === slot.start_at}
              disabled={slot.available === 0}
              onclick={() => selectSlot(slot)}
              aria-pressed={selectedStartAt === slot.start_at}
            >
              <span class="slot-time">{slot.label}</span>
            
            </button>
          {/each}
        </div>

        <div class="legend">
          <span><i class="dot dot-free"></i>Disponible</span>
          <span><i class="dot dot-sel"></i>Sélectionné</span>
          <span><i class="dot dot-full"></i>Complet</span>
        </div>

      </div>

      <!-- 2. Informations personnelles -->
      <div class="section-bar"></div>
      <div class="section-head"><h2>2 — Vos informations</h2></div>
      <div class="section-body">
        <div class="grid">

          <div class="field">
            <label for="firstName">Prénom <span class="req">*</span></label>
            <input id="firstName" type="text" bind:value={form.firstName}
              placeholder="Marie" autocomplete="given-name" />
          </div>

          <div class="field">
            <label for="lastName">Nom <span class="req">*</span></label>
            <input id="lastName" type="text" bind:value={form.lastName}
              placeholder="Tremblay" autocomplete="family-name" />
          </div>

          <div class="field">
            <label for="email">Courriel <span class="req">*</span></label>
            <input id="email" type="email" bind:value={form.email}
              placeholder="marie@exemple.com" autocomplete="email" />
          </div>

          <div class="field">
            <label for="phone">Téléphone</label>
            <input id="phone" type="tel" bind:value={form.phone}
              placeholder="514 555-0000" autocomplete="tel" />
          </div>

        </div>
      </div>

      <!-- 3. Objet à réparer -->
      <div class="section-bar"></div>
      <div class="section-head"><h2>3 — L'objet à réparer</h2></div>
      <div class="section-body">
        <div class="grid">

          <div class="field full">
            <label for="item">Nom de l'objet <span class="req">*</span></label>
            <input id="item" type="text" bind:value={form.item}
              placeholder="ex : Grille-pain Cuisinart CPT-122" />
          </div>

          <div class="field full">
            <label for="itemDescription">Description du bris <span class="req">*</span></label>
            <textarea id="itemDescription" bind:value={form.itemDescription} rows="4"
              placeholder="ex : Ne chauffe plus, bouton coincé, câble effiloché…"></textarea>
          </div>

        </div>
      </div>

      <!-- 4. Décharge -->
      <div class="section-bar"></div>
      <div class="section-head"><h2>4 — Décharge de responsabilité</h2></div>
      <div class="section-body">
        <div class="waiver-text" tabindex="0">{waiverText}</div>
        <label class="waiver-check">
          <input type="checkbox" bind:checked={form.waiverAccepted} />
          <span>J'ai lu et j'accepte la décharge de responsabilité. <strong>Obligatoire.</strong></span>
        </label>
      </div>

      {#if submitError}
        <div class="alert-error" role="alert">{submitError}</div>
      {/if}

      <button class="btn-submit" onclick={handleSubmit}>
        Confirmer la réservation
      </button>
      <p class="note">Aucun compte requis · Données supprimées après l'événement</p>

    {/if}
  </div>
</div>

<style>
  /* ── Variables  */
  

  /* ── Reset  */
  * { box-sizing: border-box; margin: 0; padding: 0; }

  /* ── Page  */
  .page {
    min-height: 100vh;
    background: var(--bg);
    font-family: var(--fb);
    color: var(--white);
  }

  /* ── Topbar  */
  .topbar {
    background: var(--card);
    border-bottom: 3px solid transparent;
    border-image: linear-gradient(to right, #7b1a2e, #c0392b, #e8455a, #c0392b, #7b1a2e) 1;
    padding: .75rem 2.5rem;
  }
  .logo {
    font-family: var(--fh);
    font-size: 1.1rem; font-weight: 700;
    letter-spacing: .08em; text-transform: uppercase;
    color: var(--white);
  }
  .logo em { color: var(--teal); font-style: normal; }

  /* ── Hero  */
  .hero {
    background: var(--card);
    padding: 2.5rem 2.5rem 2rem;
    border-bottom: 4px solid var(--red);
  }
  .hero-title {
    font-family: var(--fh);
    font-size: clamp(1.6rem, 4vw, 2.6rem);
    font-weight: 800; text-transform: uppercase;
    letter-spacing: .04em; line-height: 1.1;
    color: var(--white);
  }
  .hero-title em { color: var(--teal); font-style: normal; }

  .event-badge {
    display: inline-flex; align-items: center; gap: .5rem;
    margin-top: 1rem;
    background: rgba(0,201,177,.08);
    border: 1px solid rgba(0,201,177,.3);
    border-radius: var(--r);
    padding: .4rem .9rem;
    font-family: var(--fm); font-size: .78rem;
    color: var(--teal);
  }

  .hero-sub {
    margin-top: .75rem;
    color: var(--muted); font-size: .9rem; line-height: 1.6;
  }

  /* ── Contenu  */
  .content {
    max-width: 860px;
    margin: 0 auto;
    padding: 2rem 1.5rem 4rem;
  }

  /* ── Sections — barre teal uniforme ─ */
  .section-bar {
    height: 4px;
    background: var(--teal);       /* même couleur pour toutes les sections */
  }
  .section-head {
    background: var(--card);
    padding: .7rem 1.2rem;
    border-bottom: 1px solid var(--border);
  }
  .section-head h2 {
    font-family: var(--fh);
    font-size: .85rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: .12em;
    color: var(--white);           /* titre de section en blanc */
  }
  .section-body {
    background: var(--card);
    border: 1px solid var(--border);
    border-top: none;
    padding: 1.4rem;
    margin-bottom: 1.5rem;
  }

  /* ── Slots */
  .slot-recap {
    display: flex; align-items: center; gap: .6rem;
    margin-bottom: 1rem;
    padding: .65rem .9rem;
    background: rgba(0,201,177,.08);
    border: 1px solid rgba(0,201,177,.25);
    border-radius: var(--r);
    font-family: var(--fm); font-size: .88rem;
    color: var(--white);
  }
  .slot-recap strong { color: var(--teal); }

  .slots-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(90px, 1fr));
    gap: .5rem;
  }

  .slot-btn {
    padding: .55rem .4rem;
    background: rgba(0,201,177,.06);
    border: 1px solid rgba(0,201,177,.25);
    border-radius: var(--r);
    color: var(--white);
    font-family: var(--fm); font-size: .78rem;
    text-align: center; cursor: pointer;
    transition: all .15s;
  }
  .slot-btn:hover:not(:disabled) {
    background: rgba(0,201,177,.15);
    border-color: var(--teal);
  }
  .slot-btn.selected {
    background: var(--teal);
    border-color: var(--teal);
    color: #0e1117; font-weight: 700;
  }
  .slot-btn:disabled {
    background: transparent;
    border-color: var(--border);
    color: var(--muted);
    cursor: not-allowed; opacity: .5;
  }
  .slot-time  { display: block; font-weight: 600; }
  .slot-avail { display: block; font-size: .62rem; margin-top: 2px; color: var(--muted); }
  .slot-btn.selected .slot-avail { color: rgba(14,17,23,.65); }

  .legend {
    display: flex; gap: 1.25rem; flex-wrap: wrap;
    margin-top: .9rem;
    font-family: var(--fm); font-size: .7rem; color: var(--muted);
  }
  .dot {
    display: inline-block;
    width: 9px; height: 9px;
    border-radius: 2px; margin-right: 4px;
    vertical-align: middle; font-style: normal;
  }
  .dot-free { background: rgba(0,201,177,.15); border: 1px solid rgba(0,201,177,.4); }
  .dot-sel  { background: var(--teal); }
  .dot-full { background: transparent; border: 1px solid var(--border); }

  /* ── Formulaire  */
  .grid { display: grid; grid-template-columns: 1fr 1fr; gap: .9rem; }
  @media (max-width: 520px) { .grid { grid-template-columns: 1fr; } }
  .full { grid-column: 1 / -1; }

  .field { display: flex; flex-direction: column; gap: .3rem; }

  label {
    font-family: var(--fm);
    font-size: .68rem; font-weight: 600;
    letter-spacing: .1em; text-transform: uppercase;
    color: var(--white);           /* labels en blanc */
  }
  .req { color: var(--teal); margin-left: 2px; }

  input, textarea {
    width: 100%; padding: .6rem .85rem;
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: var(--r);
    font-family: var(--fb); font-size: .95rem;
    color: var(--white);           
    outline: none; transition: border-color .15s;
  }
  input::placeholder, textarea::placeholder { color: var(--muted); }
  input:focus, textarea:focus {
    border-color: var(--teal);
    box-shadow: 0 0 0 2px rgba(0,201,177,.12);
  }
  textarea { resize: vertical; min-height: 80px; line-height: 1.5; }

  /* ── Décharge  */
  .waiver-text {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: var(--r);
    padding: .9rem; font-size: .875rem;
    line-height: 1.65; 
    max-height: 140px; overflow-y: auto; margin-bottom: 1rem;
  }
  .waiver-check {
    display: flex; align-items: flex-start; gap: .7rem; cursor: pointer;
  }
  .waiver-check input[type="checkbox"] {
    width: 16px; height: 16px;
    flex-shrink: 0; margin-top: 3px;
    accent-color: var(--teal); cursor: pointer;
  }
  .waiver-check span { font-size: .9rem; line-height: 1.5; color: var(--muted); }
  .waiver-check strong { color: var(--white); }

  /* ── Alertes */
  .alert-error {
    padding: .85rem 1.1rem; margin-bottom: 1.25rem;
    border-radius: var(--r);
    background: rgba(192,57,43,.12);
    border-left: 4px solid var(--red);
    color: #e57373; font-size: .9rem;
  }
  .alert-success {
    background: rgba(0,201,177,.08);
    border: 1px solid var(--teal);
    border-radius: var(--r);
    color: var(--white);
    text-align: center; padding: 2.5rem 2rem;
    margin-bottom: 1.5rem;
  }
  .alert-success h2 {
    font-family: var(--fh);
    font-size: 1.6rem; font-weight: 800;
    text-transform: uppercase; letter-spacing: .05em;
    color: var(--teal); margin-bottom: .5rem;
  }
  .alert-success p  { color: var(--muted); line-height: 1.6; }
  .alert-success strong { color: var(--white); }

  /* ── Bouton  */
   .btn-submit {
    width: 100%; padding: .85rem;
    background: linear-gradient(135deg, #7b1a2e 0%, #c0392b 40%, #e8455a 70%, #9b2335 100%);
    color: var(--white); border: none;
    border-radius: 6px;
    font-family: var(--fh); font-size: 1rem; font-weight: 700;
    letter-spacing: .1em; text-transform: uppercase;
    cursor: pointer; transition: filter .15s, transform .1s;
  }
  .btn-submit:hover { filter: brightness(1.12); transform: translateY(-1px); }
 
  .note {
    text-align: center; margin-top: .6rem;
    font-family: var(--fm); font-size: .68rem;
    color: var(--muted); letter-spacing: .05em;
  }

  /* ── Responsive  */
  @media (max-width: 600px) {
    .hero          { padding: 1.5rem 1rem 1.25rem; }
    .section-body  { padding: 1rem; }
    .slots-grid    { grid-template-columns: repeat(3, 1fr); }
  }
</style>