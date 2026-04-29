<script lang="ts">
	import Header from '../../components/common/Header.svelte';
	import Sidebar from '../../components/common/Sidebar.svelte';
</script>

<Header />

<div class="admin-layout">
	<Sidebar />
	<main class="admin-content">
		<slot />
	</main>
</div>

<style>
	.admin-layout {
		display: flex;
		min-height: calc(100vh - 60px);
		background-color: #f5f5f5;
	}

	.admin-content {
		flex: 1;
		padding: 2.5rem;
	}

	@media screen and (max-width: 600px) {
		.admin-content {
			padding: 1.5rem 1rem;
		}
	}
</style>