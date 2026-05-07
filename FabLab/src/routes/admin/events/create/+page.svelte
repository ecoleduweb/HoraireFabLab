<script lang="ts">
  import { base } from '$app/paths';
  import CreateandModifyForm from '../../../../components/RepairEvent/CreateandModifyForm.svelte';
</script>

<div class="page-header">
  <a href={`${base}/admin`} class="back-link">← Retour</a>
  <h1>Créer un événement</h1>
  <p class="page-desc">Remplissez les informations pour créer une nouvelle journée d'événement.</p>
</div>

<CreateandModifyForm repairEventToEdit={null}  />

<style>
  .back-link {
    display: inline-block;
    font-family: var(--fb);
    font-size: 13px;
    color: #888;
    text-decoration: none;
    margin-bottom: 0.75rem;
    transition: color 0.15s;
  }
  .back-link:hover { color: #00ad9a; }

  .page-header { margin-bottom: 2rem; }
  .page-header h1 {
    font-family: var(--fh); font-weight: 900;
    font-size: 28px;
    color: #333;
    margin: 0 0 6px;
  }
  .page-desc {
    font-family: var(--fb);
    font-size: 15px;
    color: #888;
    margin: 0;
  }
</style>