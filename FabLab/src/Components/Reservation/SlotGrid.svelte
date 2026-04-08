<script lang="ts">

  import type { TimeSlot } from "../../modeles/Reservation.tss";

  interface Props {
    slots:           TimeSlot[];
    selectedStartAt: string;
    onSelect:        (slot: TimeSlot) => void;
  }

  let { slots, selectedStartAt, onSelect }: Props = $props();
</script>

{#if selectedStartAt}
  {@const sel = slots.find(s => s.start_at === selectedStartAt)}
  {#if sel}
    <div class="recap" role="status">
       Sélectionné : <strong>{sel.label}</strong>
      &nbsp;·&nbsp;{sel.available} place{sel.available > 1 ? 's' : ''} restante{sel.available > 1 ? 's' : ''}
    </div>
  {/if}
{/if}

<div class="grid" role="group" aria-label="Créneaux disponibles">
  {#each slots as slot (slot.start_at)}
    <button
      class="slot"
      class:selected={selectedStartAt === slot.start_at}
      disabled={slot.available === 0}
      onclick={() => onSelect(slot)}
      aria-pressed={selectedStartAt === slot.start_at}
      aria-label="{slot.label} — {slot.available === 0 ? 'Complet' : slot.available + ' place(s)'}"
    >
      <span class="time">{slot.label}</span>
      <span class="avail">
        {#if slot.available === 0}Complet{:else}{slot.available}/{slot.capacity}{/if}
      </span>
    </button>
  {/each}
</div>

<div class="legend">
  <span><i class="dot free"></i>Disponible</span>
  <span><i class="dot sel"></i>Sélectionné</span>
  <span><i class="dot full"></i>Complet</span>
</div>

<style>
  .recap {
    display: flex; align-items: center; gap: .6rem;
    margin-bottom: 1rem; padding: .65rem .9rem;
    background: rgba(0,201,177,.08);
    border: 1px solid rgba(0,201,177,.25);
    border-radius: 3px;
    font-family: 'JetBrains Mono', monospace; font-size: .88rem;
    color: #ffffff;
  }
  .recap strong { color: #00c9b1; }

  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(90px, 1fr));
    gap: .5rem;
  }

  .slot {
    padding: .55rem .4rem;
    background: rgba(0,201,177,.06);
    border: 1px solid rgba(0,201,177,.25);
    border-radius: 3px;
    color: #ffffff;
    font-family: 'JetBrains Mono', monospace; font-size: .78rem;
    text-align: center; cursor: pointer; transition: all .15s;
  }
  .slot:hover:not(:disabled) {
    background: rgba(0,201,177,.15);
    border-color: #00c9b1;
  }
  .slot.selected {
    background: #00c9b1; border-color: #00c9b1;
    color: #0e1117; font-weight: 700;
  }
  .slot:disabled {
    background: transparent; border-color: #2a3347;
    color: #7a8599; cursor: not-allowed; opacity: .5;
  }
  .time  { display: block; font-weight: 600; }
  .avail { display: block; font-size: .62rem; margin-top: 2px; color: #7a8599; }
  .slot.selected .avail { color: rgba(14,17,23,.65); }

  .legend {
    display: flex; gap: 1.25rem; flex-wrap: wrap;
    margin-top: .9rem;
    font-family: 'JetBrains Mono', monospace; font-size: .7rem; color: #7a8599;
  }
  .dot {
    display: inline-block; width: 9px; height: 9px;
    border-radius: 2px; margin-right: 4px; vertical-align: middle;
    font-style: normal;
  }
  .free { background: rgba(0,201,177,.15); border: 1px solid rgba(0,201,177,.4); }
  .sel  { background: #00c9b1; }
  .full { background: transparent; border: 1px solid #2a3347; }

  @media (max-width: 600px) {
    .grid { grid-template-columns: repeat(3, 1fr); }
  }
</style>