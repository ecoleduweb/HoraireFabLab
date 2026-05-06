<script lang="ts">
  interface Props {
    error?: string
  }

let { error }: Props = $props()
let accepted = $state(false)


  const liabilityText = `Les ateliers de réparation sont des événements communautaires sans buts lucratifs dont le but est de lutter contre l'obsolescence planifiée et de diminuer l'impact environnemental des biens de consommation courantes en prolongeant leur durée de vie utile. Les bénévoles réparateurs n'interviennent pas en tant que professionnels, mais en tant que bénévoles plus expérimentés que moi pour m'accompagner dans mon processus de réparation. 
    
    Assisté par des bénévoles, j'apprendrai à réparer les objets que j'aurai apportés. 
    Je comprends que : 
    - « Répare TES trucs » est un événement d'auto-reparation communautaire ; 
    - participer signifie que j'assume la responsabilité de mon objet; 
    - les bénévoles réparateurs sont disponibles pour la journée seulement et n'offrent pas de services de réparation en dehors de l'événement; 
    
    Je dégage de toute responsabilité en cas d'accident de quelque nature que ce soit ou de dommage, sans aucune exception ni aucune réserve, les organisateurs de l'événement ainsi que toutes les personnes bénévoles œuvrant à l'événement. `
</script>

<div class="waiver-text" tabindex="0">{liabilityText}</div>

<label class="check-wrap" 
  for="liabilityAccepted"
>
  <input
    id="liabilityAccepted"
    data-testid="liability-checkbox"
    bind:checked={accepted}
    type="checkbox"
    name="liabilityAccepted"
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
    font-size: .875rem;
    line-height: 1.65;
    color: #7a8599;
    max-height: 140px;
    overflow-y: auto;
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