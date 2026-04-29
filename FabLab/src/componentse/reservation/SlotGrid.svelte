<script lang="ts">
  import type { TimeSlot } from '../../models/TimeSlot.ts'
  import { displayTime }   from '../../ts/displayUtils.ts'

  interface Props {
    slots:           TimeSlot[]
    selectedStartAt: string
    onSelect:        (slot: TimeSlot) => void
  }

  let { slots, selectedStartAt, onSelect }: Props = $props()

  function handleChange(slot: TimeSlot) {
    onSelect(slot)
  }
</script>

{#if selectedStartAt}
  {@const sel = slots.find(s => s.startAt === selectedStartAt)}
  {#if sel}
    <div class="recap" role="status">
       Sélectionné : <strong>{displayTime(sel.startAt)}</strong>
    </div>
  {/if}
{/if}

<fieldset class="grid" role="radiogroup" aria-label="Créneaux disponibles">
  <legend class="sr-only">Choisissez une plage horaire</legend>

  {#each slots as slot (slot.startAt)}
    <label
      class="slot"
      class:selected={selectedStartAt === slot.startAt}
    >
      <input
        type="radio"
        name="selectedSlot"
        value={slot.startAt}
        checked={selectedStartAt === slot.startAt}
        onchange={() => handleChange(slot)}
        class="sr-only"
      />
      <span class="time">{displayTime(slot.startAt)}</span>
    </label>
  {/each}
</fieldset>

<style>
  .sr-only {
    position: absolute; width: 1px; height: 1px;
    padding: 0; margin: -1px; overflow: hidden;
    clip: rect(0,0,0,0); white-space: nowrap; border: 0;
  }

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

  fieldset {
    border: none; padding: 0; margin: 0;
  }

  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(90px, 1fr));
    gap: .5rem;
  }

  .slot {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: .55rem .4rem;
    background: rgba(0,201,177,.06);
    border: 1px solid rgba(0,201,177,.25);
    border-radius: 3px;
    color: #ffffff;
    font-family: 'JetBrains Mono', monospace; font-size: .78rem;
    text-align: center; cursor: pointer; transition: all .15s;
  }
  .slot:hover {
    background: rgba(0,201,177,.15);
    border-color: #00c9b1;
  }
  .slot:has(input:focus-visible) {
    outline: 2px solid #00c9b1;
    outline-offset: 2px;
  }
  .slot.selected {
    background: #00c9b1; border-color: #00c9b1;
    color: #0e1117; font-weight: 700;
  }

  .time { display: block; font-weight: 600; }

  @media (max-width: 600px) {
    .grid { grid-template-columns: repeat(3, 1fr); }
  }
</style>