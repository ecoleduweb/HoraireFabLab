<script lang="ts">
	import { goto } from "$app/navigation";
	import { onMount } from "svelte";

    const handleBtnClick = () => {
	    goto("/login");
	};
    
</script>

<section>
	<h1>It works!</h1>
	<button onclick={handleBtnClick}>Logout</button>
</section>