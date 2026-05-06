<script lang="ts">
  import { onMount }          from 'svelte';
  import Form                 from '../components/reservation/Form.svelte';
  import type { TimeSlot }    from '../models/TimeSlot.ts';
  import type { RepairEvent } from '../models/RepairEvent.ts';
  import { fetchActiveEvent } from '../services/EventService.ts';
  import { fetchAvailableSlots } from '../services/ReservationService.ts';
  import { displayDate }      from '../ts/displayUtils.ts';

  let eventData = $state<RepairEvent>();
  let slots     = $state<TimeSlot[]>([]);

  onMount(async () => {
    eventData = await fetchActiveEvent();
    slots     = await fetchAvailableSlots(eventData.id);
  });
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
    <!-- Form gère tout : Felte, validation, appel API, confirmation -->
    <Form {slots} />
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

  @media (max-width: 600px) {
    .hero { padding: 1.5rem 1rem 1.25rem; }
  }
</style>