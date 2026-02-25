<script lang="ts">
	import { goto } from "$app/navigation";

    const handleBtnClick = async () => {
	    await goto("/login");
	};
    
</script>

<section>
	<h1>It works!</h1>
	<button onclick={handleBtnClick}>Logout</button>
</section>