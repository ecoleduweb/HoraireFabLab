<script lang="ts">
    import Header from '../../Components/Common/Header.svelte';
    import Sidebar from '../../Components/Common/Sidebar.svelte';
    import { icons } from '../../lib/icon.ts';
</script>

<Header />

<div class="admin-layout">
    <Sidebar />

    <main class="admin-content">
        <div class="page-header">
            <h1>Administration</h1>
            <p class="page-desc">Sélectionnez une action.</p>
        </div>

        <div class="sections-grid">
            <a href="/admin/events/create" class="section-card">
                <div class="card-icon">{@html icons.calendarAdd}</div>
                <div class="card-content">
                    <h2>Créer un événement</h2>
                    <p>Ajouter une nouvelle journée d'événement au FabLab.</p>
                </div>
                <div class="card-arrow">{@html icons.chevronRight}</div>
            </a>
        </div>
    </main>
</div>

<style>
	/* ── En-tête de page ── */
	.page-header {
		margin-bottom: 2.5rem;
	}

	.page-header h1 {
		font-family: RobotoCondensed-Black;
		font-size: 28px;
		color: #333;
		margin: 0 0 6px;
	}

	.page-desc {
		font-family: RobotoCondensed-Regular;
		font-size: 15px;
		color: #888;
		margin: 0;
	}

	/* ── Cards de section ── */
	.sections-grid {
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.section-card {
		display: flex;
		align-items: center;
		gap: 1.25rem;
		background-color: #fff;
		border: 1px solid #e0e0e0;
		border-radius: 12px;
		padding: 1.25rem 1.5rem;
		text-decoration: none;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.06);
		transition: box-shadow 0.2s, border-color 0.2s, transform 0.15s;
	}

	.section-card:hover {
		border-color: #00ad9a;
		box-shadow: 0 4px 12px rgba(0, 173, 154, 0.12);
		transform: translateY(-1px);
	}

	.card-icon {
		width: 48px;
		height: 48px;
		border-radius: 10px;
		background-color: rgba(0, 173, 154, 0.08);
		color: #00ad9a;
		display: flex;
		align-items: center;
		justify-content: center;
		flex-shrink: 0;
		transition: background-color 0.2s;
	}

	.section-card:hover .card-icon {
		background-color: rgba(0, 173, 154, 0.15);
	}

	.card-content {
		flex: 1;
	}

	.card-content h2 {
		font-family: RobotoCondensed-Bold;
		font-size: 17px;
		color: #222;
		margin: 0 0 4px;
	}

	.card-content p {
		font-family: RobotoCondensed-Regular;
		font-size: 14px;
		color: #888;
		margin: 0;
	}

	.card-arrow {
		color: #ccc;
		flex-shrink: 0;
		transition: color 0.2s, transform 0.2s;
	}

	.section-card:hover .card-arrow {
		color: #00ad9a;
		transform: translateX(3px);
	}

	/* ── Layout avec sidebar ── */
	.admin-layout {
		display: flex;
		min-height: calc(100vh - 60px);
		background-color: #f5f5f5;
	}

	.admin-content {
		flex: 1;
		padding: 2.5rem;
	}

	/* ── Responsive ── */
	@media screen and (max-width: 600px) {

		.section-card {
			padding: 1rem 1.25rem;
		}

		.admin-content {
			padding: 1.5rem 1rem;
		}
	}
</style>