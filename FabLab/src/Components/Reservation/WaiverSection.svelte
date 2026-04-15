<script lang="ts">

  interface Props {
    accepted: boolean;   
    error?:   string;   
  }

  let { accepted = $bindable(), error }: Props = $props();

  // Texte de la décharge
  // TODO éventuellement: charger depuis GET /api/waiver-text/ 
  const waiverText = `En participant à cet atelier de réparation organisé par le FabLab Fabbulle,
je reconnais avoir été informé(e) que les bénévoles présents ne sont pas des techniciens
professionnels certifiés. Je comprends que la réparation de mon objet n'est pas garantie
et que le FabLab Fabbulle ne pourra être tenu responsable de tout dommage supplémentaire
survenant pendant ou après l'atelier. Je participe à cet événement volontairement et en
pleine connaissance de ces conditions.`;
</script>

<div class="waiver-text" tabindex="0" aria-label="Texte de la décharge de responsabilité">
  {waiverText}
</div>

<label class="check-wrap">
  <input
    type="checkbox"
    data-testid="waiver-checkbox"
    bind:checked={accepted}
    aria-required="true"
    class:invalid={!!error}
  />
  <span>
    J'ai lu et j'accepte la décharge de responsabilité.
    <strong>Obligatoire.</strong>
  </span>
</label>

{#if error}
  <span class="err">{error}</span>
{/if}

<style>
  .waiver-text {
    background: #0e1117;
    border: 1px solid #2a3347;
    border-radius: 3px;
    padding: .9rem;
    font-size: .875rem; line-height: 1.65;
    color: #7a8599;
    max-height: 140px; overflow-y: auto;
    margin-bottom: 1rem;
    white-space: pre-line;
  }

  .check-wrap {
    display: flex; align-items: flex-start;
    gap: .7rem; cursor: pointer;
  }
  .check-wrap input[type="checkbox"] {
    width: 16px; height: 16px;
    flex-shrink: 0; margin-top: 3px;
    accent-color: #00c9b1; cursor: pointer;
  }
  .check-wrap input.invalid { outline: 2px solid #e8455a; }
  .check-wrap span { font-size: .9rem; line-height: 1.5; color: #7a8599; }
  .check-wrap strong { color: #ffffff; }

  .err {
    display: block; margin-top: .4rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: .68rem; color: #e8455a;
  }
</style>